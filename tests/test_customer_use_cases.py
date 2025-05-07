import pytest
from unittest.mock import MagicMock

from app.application.use_cases.customer_use_cases import CustomerUseCases
from app.domain.entities.customer import Customer, CustomerDb
from app.domain.interfaces.customer_repository import CustomerRepository


class TestCustomerUseCases:
    def setup_method(self):
        self.mock_repo = MagicMock(spec=CustomerRepository)
        self.use_cases = CustomerUseCases(self.mock_repo)

    def test_get_all_customers(self):
        customers = [
            CustomerDb(id=1, name="John", cpf="12345678901", email="john@example.com", created_at=None, updated_at=None),
            CustomerDb(id=2, name="Jane", cpf="10987654321", email="jane@example.com", created_at=None, updated_at=None)
        ]
        self.mock_repo.get_all.return_value = customers

        result = self.use_cases.get_all_customers()

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        self.mock_repo.get_all.assert_called_once()

    def test_get_customer_by_id(self):
        customer = CustomerDb(id=1, name="John", cpf="12345678901", email="john@example.com", created_at=None, updated_at=None)
        self.mock_repo.get_by_id.return_value = customer

        result = self.use_cases.get_customer_by_id(1)

        assert result.id == 1
        assert result.name == "John"
        self.mock_repo.get_by_id.assert_called_once_with(1)
        
    def test_get_customer_by_id_not_found(self):
        self.mock_repo.get_by_id.return_value = None

        result = self.use_cases.get_customer_by_id(999)

        assert result is None
        self.mock_repo.get_by_id.assert_called_once_with(999)
        
    def test_create_customer(self):
        customer = Customer(name="New Customer", cpf="11122233344", email="new@example.com")
        created_customer = CustomerDb(
            id=3, name="New Customer", cpf="11122233344", email="new@example.com", 
            created_at=None, updated_at=None
        )
        self.mock_repo.get_by_cpf.return_value = None
        self.mock_repo.create.return_value = created_customer

        result = self.use_cases.create_customer(customer)

        assert result.id == 3
        self.mock_repo.get_by_cpf.assert_called_once_with("11122233344")
        self.mock_repo.create.assert_called_once()
        
    def test_create_customer_duplicate_cpf(self):
        customer = Customer(name="New Customer", cpf="11122233344", email="new@example.com")
        existing = CustomerDb(
            id=3, name="Existing", cpf="11122233344", email="existing@example.com", 
            created_at=None, updated_at=None
        )
        self.mock_repo.get_by_cpf.return_value = existing

        with pytest.raises(ValueError, match=f"Customer with CPF {customer.cpf} already exists"):
            self.use_cases.create_customer(customer)
        
        self.mock_repo.get_by_cpf.assert_called_once_with("11122233344")
        self.mock_repo.create.assert_not_called()
        
    def test_update_customer(self):
        customer_id = 1
        customer = Customer(name="Updated Customer", cpf="12345678901", email="updated@example.com")
        existing = CustomerDb(
            id=customer_id, name="Existing", cpf="12345678901", email="existing@example.com", 
            created_at=None, updated_at=None
        )
        updated = CustomerDb(
            id=customer_id, name="Updated Customer", cpf="12345678901", email="updated@example.com", 
            created_at=None, updated_at=None
        )
        self.mock_repo.get_by_id.return_value = existing
        self.mock_repo.update.return_value = updated

        result = self.use_cases.update_customer(customer_id, customer)

        assert result.id == customer_id
        assert result.name == "Updated Customer"
        self.mock_repo.get_by_id.assert_called_once_with(customer_id)
        self.mock_repo.update.assert_called_once_with(customer_id, customer)
        
    def test_delete_customer(self):
        customer_id = 1
        self.mock_repo.delete.return_value = True

        result = self.use_cases.delete_customer(customer_id)

        assert result is True
        self.mock_repo.delete.assert_called_once_with(customer_id) 
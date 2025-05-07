from typing import List, Optional

from app.domain.entities.customer import Customer, CustomerDb
from app.domain.interfaces.customer_repository import CustomerRepository


class CustomerUseCases:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_all_customers(self) -> List[CustomerDb]:
        return self.repository.get_all()

    def get_customer_by_id(self, customer_id: int) -> Optional[CustomerDb]:
        return self.repository.get_by_id(customer_id)

    def get_customer_by_cpf(self, cpf: str) -> Optional[CustomerDb]:
        return self.repository.get_by_cpf(cpf)

    def create_customer(self, customer: Customer) -> CustomerDb:
        # Check if customer with same CPF already exists
        existing = self.repository.get_by_cpf(customer.cpf)
        if existing:
            raise ValueError(f"Customer with CPF {customer.cpf} already exists")
        
        return self.repository.create(customer)

    def update_customer(self, customer_id: int, customer: Customer) -> Optional[CustomerDb]:
        # Check if customer exists
        existing = self.repository.get_by_id(customer_id)
        if not existing:
            return None
        
        # Check if CPF is being changed and if new CPF already exists
        if existing.cpf != customer.cpf:
            cpf_exists = self.repository.get_by_cpf(customer.cpf)
            if cpf_exists:
                raise ValueError(f"Customer with CPF {customer.cpf} already exists")
        
        return self.repository.update(customer_id, customer)

    def delete_customer(self, customer_id: int) -> bool:
        return self.repository.delete(customer_id) 
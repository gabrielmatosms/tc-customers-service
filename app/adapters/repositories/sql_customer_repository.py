from typing import List, Optional

from sqlalchemy.orm import Session

from app.adapters.models.sql.customer_model import CustomerModel
from app.domain.entities.customer import Customer, CustomerDb
from app.domain.interfaces.customer_repository import CustomerRepository


class SQLCustomerRepository(CustomerRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self) -> List[CustomerDb]:
        customers = self.db_session.query(CustomerModel).all()
        return [self._map_to_entity(customer) for customer in customers]

    def get_by_id(self, customer_id: int) -> Optional[CustomerDb]:
        customer = self.db_session.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
        return self._map_to_entity(customer) if customer else None

    def get_by_cpf(self, cpf: str) -> Optional[CustomerDb]:
        customer = self.db_session.query(CustomerModel).filter(CustomerModel.cpf == cpf).first()
        return self._map_to_entity(customer) if customer else None

    def create(self, customer: Customer) -> CustomerDb:
        db_customer = CustomerModel(
            name=customer.name,
            cpf=customer.cpf,
            email=customer.email,
        )
        self.db_session.add(db_customer)
        self.db_session.commit()
        self.db_session.refresh(db_customer)
        return self._map_to_entity(db_customer)

    def update(self, customer_id: int, customer: Customer) -> Optional[CustomerDb]:
        db_customer = self.db_session.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
        if not db_customer:
            return None
        
        db_customer.name = customer.name
        db_customer.cpf = customer.cpf
        db_customer.email = customer.email
        
        self.db_session.commit()
        self.db_session.refresh(db_customer)
        return self._map_to_entity(db_customer)

    def delete(self, customer_id: int) -> bool:
        db_customer = self.db_session.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
        if not db_customer:
            return False
        
        self.db_session.delete(db_customer)
        self.db_session.commit()
        return True
    
    def _map_to_entity(self, model: CustomerModel) -> CustomerDb:
        return CustomerDb(
            id=model.id,
            name=model.name,
            cpf=model.cpf,
            email=model.email,
            created_at=model.created_at,
            updated_at=model.updated_at,
        ) 
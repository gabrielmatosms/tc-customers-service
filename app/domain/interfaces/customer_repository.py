from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.customer import Customer, CustomerDb


class CustomerRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[CustomerDb]:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[CustomerDb]:
        pass

    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Optional[CustomerDb]:
        pass

    @abstractmethod
    def create(self, customer: Customer) -> CustomerDb:
        pass

    @abstractmethod
    def update(self, customer_id: int, customer: Customer) -> Optional[CustomerDb]:
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> bool:
        pass 
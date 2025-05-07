from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pymongo.collection import Collection

from app.adapters.models.nosql.connection import customer_collection
from app.domain.entities.customer import Customer, CustomerDb
from app.domain.interfaces.customer_repository import CustomerRepository


class NoSQLCustomerRepository(CustomerRepository):
    def __init__(self, collection: Collection = customer_collection):
        self.collection = collection

    def get_all(self) -> List[CustomerDb]:
        customers = list(self.collection.find())
        return [self._map_to_entity(customer) for customer in customers]

    def get_by_id(self, customer_id: int) -> Optional[CustomerDb]:
        customer = self.collection.find_one({"_id": customer_id})
        return self._map_to_entity(customer) if customer else None

    def get_by_cpf(self, cpf: str) -> Optional[CustomerDb]:
        customer = self.collection.find_one({"cpf": cpf})
        return self._map_to_entity(customer) if customer else None

    def create(self, customer: Customer) -> CustomerDb:
        # Find the highest id to simulate auto-increment
        last_customer = self.collection.find_one(sort=[("_id", -1)])
        next_id = 1 if not last_customer else last_customer["_id"] + 1
        
        now = datetime.utcnow()
        customer_dict = {
            "_id": next_id,
            "name": customer.name,
            "cpf": customer.cpf,
            "email": customer.email,
            "created_at": now,
            "updated_at": now
        }
        
        self.collection.insert_one(customer_dict)
        return self._map_to_entity(customer_dict)

    def update(self, customer_id: int, customer: Customer) -> Optional[CustomerDb]:
        now = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": customer_id},
            {"$set": {
                "name": customer.name,
                "cpf": customer.cpf,
                "email": customer.email,
                "updated_at": now
            }}
        )
        
        if result.modified_count == 0:
            return None
            
        return self.get_by_id(customer_id)

    def delete(self, customer_id: int) -> bool:
        result = self.collection.delete_one({"_id": customer_id})
        return result.deleted_count > 0
    
    def _map_to_entity(self, data: dict) -> CustomerDb:
        return CustomerDb(
            id=data["_id"],
            name=data["name"],
            cpf=data["cpf"],
            email=data.get("email"),
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        ) 
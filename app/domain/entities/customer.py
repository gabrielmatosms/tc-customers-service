from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    cpf: str
    email: Optional[str] = None


class CustomerDb(Customer):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 
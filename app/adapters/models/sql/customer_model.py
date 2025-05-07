from sqlalchemy import Column, String

from app.adapters.models.sql.base import BaseModel


class CustomerModel(BaseModel):
    __tablename__ = "customers"

    name = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True) 
from enum import Enum
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.interfaces.customer_repository import CustomerRepository
from .sql_customer_repository import SQLCustomerRepository


class RepositoryType(str, Enum):
    SQL = "sql"


def get_customer_repository(
    repository_type: RepositoryType, db_session: Optional[Session] = None
) -> CustomerRepository:
    if repository_type == RepositoryType.SQL:
        if not db_session:
            raise ValueError("DB session is required for SQL repository")
        return SQLCustomerRepository(db_session)

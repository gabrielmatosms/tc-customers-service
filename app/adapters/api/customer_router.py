from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.adapters.models.sql.session import get_db
from app.adapters.repositories import RepositoryType, get_customer_repository
from app.application.use_cases.customer_use_cases import CustomerUseCases
from app.domain.entities.customer import Customer, CustomerDb

router = APIRouter()

# Helper function to get customer use cases with SQL repository
def get_customer_use_cases(db: Session = Depends(get_db)) -> CustomerUseCases:
    repository = get_customer_repository(RepositoryType.SQL, db)
    return CustomerUseCases(repository)


@router.get("/", response_model=List[CustomerDb])
def get_all_customers(use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    return use_cases.get_all_customers()


@router.get("/{customer_id}", response_model=CustomerDb)
def get_customer(customer_id: int, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    customer = use_cases.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    return customer


@router.get("/cpf/{cpf}", response_model=CustomerDb)
def get_customer_by_cpf(cpf: str, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    customer = use_cases.get_customer_by_cpf(cpf)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with CPF {cpf} not found"
        )
    return customer


@router.post("/", response_model=CustomerDb, status_code=status.HTTP_201_CREATED)
def create_customer(customer: Customer, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    try:
        return use_cases.create_customer(customer)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{customer_id}", response_model=CustomerDb)
def update_customer(
    customer_id: int, customer: Customer, use_cases: CustomerUseCases = Depends(get_customer_use_cases)
):
    try:
        updated_customer = use_cases.update_customer(customer_id, customer)
        if not updated_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        return updated_customer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    deleted = use_cases.delete_customer(customer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        ) 
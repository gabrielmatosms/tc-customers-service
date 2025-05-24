import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from main import app
from app.adapters.models.sql.base import Base
from app.adapters.models.sql.session import get_db

@pytest.fixture(scope="function")
def client():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_url = f"sqlite:///{tmp.name}"
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)

        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as c:
            yield c
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        os.unlink(tmp.name)

def test_create_and_get_customer(client):
    # Cria um novo cliente
    response = client.post("/api/v1/customers/", json={
        "name": "Cliente Teste",
        "cpf": "12345678900",
        "email": "teste@exemplo.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Cliente Teste"
    assert data["cpf"] == "12345678900"
    customer_id = data["id"]

    # Busca todos os clientes
    response = client.get("/api/v1/customers/")
    assert response.status_code == 200
    customers = response.json()
    assert len(customers) == 1
    assert customers[0]["id"] == customer_id

    # Busca por ID
    response = client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["cpf"] == "12345678900"

    # Busca por CPF
    response = client.get(f"/api/v1/customers/cpf/12345678900")
    assert response.status_code == 200
    assert response.json()["name"] == "Cliente Teste"

def test_update_customer(client):
    # Cria um cliente
    response = client.post("/api/v1/customers/", json={
        "name": "Cliente Teste",
        "cpf": "12345678900",
        "email": "teste@exemplo.com"
    })
    customer_id = response.json()["id"]

    # Atualiza o cliente
    response = client.put(f"/api/v1/customers/{customer_id}", json={
        "name": "Cliente Atualizado",
        "cpf": "12345678900",
        "email": "novo@exemplo.com"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Cliente Atualizado"
    assert response.json()["email"] == "novo@exemplo.com"

def test_delete_customer(client):
    # Cria um cliente
    response = client.post("/api/v1/customers/", json={
        "name": "Cliente Teste",
        "cpf": "12345678900",
        "email": "teste@exemplo.com"
    })
    customer_id = response.json()["id"]

    # Deleta o cliente
    response = client.delete(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 204

    # Verifica que não existe mais
    response = client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 404 
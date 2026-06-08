import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import CodeHistory

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_generate_qr_success():
    response = client.post("/generate/qr", json={
        "data": "https://example.com",
        "fill_color": "black",
        "back_color": "white"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "QR"
    assert data["image_url"].startswith("data:image/png;base64,")

def test_generate_barcode_success():
    response = client.post("/generate/barcode", json={
        "data": "123456789012",
        "barcode_type": "ean13"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "BARCODE"
    assert "image_url" in data

def test_generate_barcode_invalid_data():
    response = client.post("/generate/barcode", json={
        "data": "not-digits",
        "barcode_type": "ean13"
    })
    assert response.status_code == 400

def test_history_endpoint():
    client.post("/generate/qr", json={"data": "test history"})
    
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    
    assert "total" in data
    assert "items" in data
    assert data["total"] >= 1
    assert data["items"][0]["data"] == "test history"
    assert data["items"][0]["image_base64"] is not None 

def test_history_pagination():
    # Dodajemy 3 wpisy
    for i in range(3):
        client.post("/generate/qr", json={"data": f"test {i}"})
        
    response = client.get("/history?limit=2&skip=0")
    data = response.json()
    
    assert len(data["items"]) == 2
    assert data["total"] == 3
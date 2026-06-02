from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_generate_qr_success():
    response = client.post("/generate/qr", json={
        "data": "MojeTajneDane",
        "fill_color": "black",
        "back_color": "white"
    })
    assert response.status_code == 200
    assert response.json()["type"] == "QR"
    assert response.json()["image_url"].startswith("data:image/png;base64,")

def test_generate_qr_short_hex_color():
    response = client.post("/generate/qr", json={
        "data": "Hex3",
        "fill_color": "#F00",
        "back_color": "#00FF0080"
    })
    assert response.status_code == 200

def test_generate_qr_invalid_color():
    response = client.post("/generate/qr", json={
        "data": "Test",
        "fill_color": "niewłaściwy kolor",
        "back_color": "white"
    })
    assert response.status_code == 422

def test_generate_barcode_success():
    response = client.post("/generate/barcode", json={
        "data": "1234567890128",
        "barcode_type": "ean13"
    })
    assert response.status_code == 200
    assert response.json()["type"] == "BARCODE"

def test_history_pagination():
    client.post("/generate/qr", json={"data": "test_historia", "fill_color": "red"})
    
    response = client.get("/history?limit=1&skip=0")
    assert response.status_code == 200

    data = response.json()
    
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) <= 1

def test_generate_barcode_with_colors_success():
    response = client.post("/generate/barcode", json={
        "data": "1234567890128",
        "barcode_type": "code128",
        "fill_color": "#FF0000",
        "back_color": "#00FF00"
    })
    assert response.status_code == 200
    assert response.json()["type"] == "BARCODE"
    assert response.json()["image_url"].startswith("data:image/png;base64,")

def test_history_pagination_limits():
    client.post("/generate/qr", json={"data": "test_limitow", "fill_color": "red"})
    
    response_invalid = client.get("/history?limit=150")
    assert response_invalid.status_code == 422 

    response_valid = client.get("/history?limit=3")
    assert response_valid.status_code == 200
    assert len(response_valid.json()["items"]) <= 3

def test_generate_qr_logo_too_large():
    """Test walidacji max wielkości Base64 dla logo"""
    huge_base64 = "a" * 2_000_001
    response = client.post("/generate/qr", json={
        "data": "Test stringa",
        "logo_base64": huge_base64
    })
    assert response.status_code == 422
    assert "Przesłane logo jest zbyt duże" in str(response.json()["detail"])
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
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

INVALID_BARCODE_PAYLOADS = [
    ("ean13", "12345"),
    ("ean13", "123456789012345"), 
    ("ean13", "ABCDEFGHIJKL"),
    ("ean8", "123"),
    ("isbn13", "1234"),
    ("upca", "123"),
]

def test_generate_qr_success():
    response = client.post("/generate/qr", json={
        "data": "https://example.com",
        "fill_color": "black",
        "back_color": "white"
    })
    assert response.status_code == 200
    assert response.json()["type"] == "QR"

@pytest.mark.parametrize("b_type, b_data", [
    ("ean13", "123456789012"),
    ("code128", "WitajSwiecie123"),
    ("ean8", "1234567")
])
def test_generate_barcode_success(b_type, b_data):
    response = client.post("/generate/barcode", json={
        "data": b_data,
        "barcode_type": b_type
    })
    assert response.status_code == 200
    assert response.json()["type"] == "BARCODE"
    assert response.json()["image_url"].startswith("data:image/png;base64,")

@pytest.mark.parametrize("b_type, invalid_data", INVALID_BARCODE_PAYLOADS)
def test_generate_barcode_invalid_data_triggers_422(b_type, invalid_data):
    response = client.post("/generate/barcode", json={
        "data": invalid_data,
        "barcode_type": b_type
    })
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.parametrize("bad_color", ["nieznany_kolor!", "123", "#xyz", "#FFF123456"])
def test_generate_qr_invalid_colors(bad_color):
    response = client.post("/generate/qr", json={
        "data": "Test",
        "fill_color": bad_color
    })
    assert response.status_code == 422

def test_history_endpoint_empty():
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0

def test_history_pagination():
    for i in range(15):
        client.post("/generate/qr", json={"data": f"test {i}"})
        
    response = client.get("/history?limit=5&skip=0")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data["items"]) == 5
    assert data["total"] == 15

@pytest.mark.parametrize("skip, limit, expected_status", [
    (-1, 10, 422), 
    (0, 0, 422),   
    (0, 150, 422)   
])
def test_history_query_params_validation(skip, limit, expected_status):
    response = client.get(f"/history?skip={skip}&limit={limit}")
    assert response.status_code == expected_status
import pytest
from app.generators import QRCodeGenerator, BarcodeGenerator, LogoProcessingException

VALID_BARCODES = [
    ("code128", "ToJestTestowyTekstCode128!@#"),
    ("code128", "123456"),
    ("code39", "CODE39TEST"),
    ("ean13", "123456789012"),
    ("ean13", "1234567890128"),
    ("ean8", "1234567"),
    ("isbn13", "9781234567897"),
    ("upca", "12345678901"),
]

COLOR_COMBINATIONS = [
    ("black", "white"),
    ("red", "yellow"),
    ("#000000", "#FFFFFF"),
    ("green", "transparent"),
]

@pytest.mark.parametrize("test_data", [
    "https://example.com",
    "Krótki tekst",
    "Bardzo długi tekst" * 50,
    "Znakī śpēcjąłne"
])
def test_qr_code_generator_returns_base64(test_data):
    generator = QRCodeGenerator()
    result = generator.generate(data=test_data)
    assert isinstance(result, str)
    assert len(result) > 100

@pytest.mark.parametrize("fill, back", COLOR_COMBINATIONS)
def test_qr_code_generator_colors(fill, back):
    generator = QRCodeGenerator()
    result = generator.generate(data="TestKolorow", fill_color=fill, back_color=back)
    assert isinstance(result, str)

@pytest.mark.parametrize("b_type, data", VALID_BARCODES)
def test_barcode_generator_valid_types(b_type, data):
    generator = BarcodeGenerator()
    result = generator.generate(data=data, barcode_type=b_type)
    assert isinstance(result, str)
    assert len(result) > 100

def test_barcode_generator_handles_invalid_type_gracefully():
    generator = BarcodeGenerator()
    with pytest.raises(ValueError, match="Nieobsługiwany typ kodu kreskowego"):
        generator.generate(data="12345", barcode_type="nieistniejacy_typ")

def test_qr_code_generator_invalid_logo():
    generator = QRCodeGenerator()
    bad_logo_base64 = "ToNieJestPrawidlowyBase64Obrazka"
    with pytest.raises(LogoProcessingException, match="Nie udało się nałożyć logo na kod QR"):
        generator.generate(data="https://example.com", logo_base64=bad_logo_base64)
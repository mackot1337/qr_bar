import pytest
from app.generators import QRCodeGenerator, BarcodeGenerator, LogoProcessingException

def test_qr_code_generator_returns_base64_string():
    generator = QRCodeGenerator()
    test_data = "https://example.com"

    result = generator.generate(data=test_data)

    assert isinstance(result, str), "Wynik powinien być ciągiem znaków (string)"
    assert len(result) > 100, "Wygenerowany ciąg Base64 jest za krótki, prawdopodobnie pusty"

def test_barcode_generator_returns_base64_string():
    generator = BarcodeGenerator()
    test_data = "123456789012"

    result = generator.generate(data=test_data, barcode_type="code128")

    assert isinstance(result, str)
    assert len(result) > 100

def test_barcode_generator_handles_invalid_type_gracefully():
    generator = BarcodeGenerator()
    test_data = "12345"
    
    with pytest.raises(ValueError) as exc_info:
        generator.generate(data=test_data, barcode_type="nieistniejacy_typ")

    assert "Nieobsługiwany typ kodu kreskowego" in str(exc_info.value)

def test_barcode_generator_with_colors():
    generator = BarcodeGenerator()
    test_data = "12345"

    result = generator.generate(
        data=test_data, 
        barcode_type="code128", 
        fill_color="red", 
        back_color="blue"
    )

    assert isinstance(result, str)
    assert len(result) > 100

def test_qr_code_generator_invalid_logo():
    generator = QRCodeGenerator()
    test_data = "https://example.com"
    bad_logo_base64 = "ToNieJestPrawidlowyBase64Obrazka"

    with pytest.raises(LogoProcessingException) as exc_info:
        generator.generate(data=test_data, logo_base64=bad_logo_base64)
    
    assert "Nie udało się nałożyć logo na kod QR" in str(exc_info.value)
import base64
from io import BytesIO
from abc import ABC, abstractmethod
import qrcode
import barcode
from barcode.writer import ImageWriter

class CodeGenerator(ABC):
    @abstractmethod
    def generate(self, data: str, **kwargs) -> str:
        """Metoda do nadpisania przez konkretne generatory"""
        pass

    def _encode_to_base64(self, image_buffer: BytesIO) -> str:
        """Wspólna metoda zmieniająca bufor obrazu na tekst Base64"""
        return base64.b64encode(image_buffer.getvalue()).decode("utf-8")


class QRCodeGenerator(CodeGenerator):
    def generate(self, data: str, fill_color: str = "black", back_color: str = "white", **kwargs) -> str:

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return self._encode_to_base64(buffer)


class BarcodeGenerator(CodeGenerator):
    def generate(self, data: str, barcode_type: str = "code128", **kwargs) -> str:

        if barcode_type not in barcode.PROVIDED_BARCODES:
            barcode_type = "code128"
            
        barcode_class = barcode.get_barcode_class(barcode_type)
        writer = ImageWriter()
        
        code = barcode_class(data, writer=writer)
        
        buffer = BytesIO()
        code.write(buffer)
        return self._encode_to_base64(buffer)
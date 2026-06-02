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
    def generate(self, data: str, fill_color: str = "black", back_color: str = "white", logo_base64: str = None,**kwargs) -> str:

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

        if logo_base64:
            try:
                if "," in logo_base64:
                    logo_base64 = logo_base64.split(",")[1]
                        
                logo_bytes = base64.b64decode(logo_base64)
                logo = Image.open(BytesIO(logo_bytes))
                
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')

                basewidth = int(img.size[0] / 4)
                wpercent = (basewidth / float(logo.size[0]))
                hsize = int((float(logo.size[1]) * float(wpercent)))
                logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                
                pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, pos, mask=logo)
            except Exception as e:
                print(f"Błąd podczas wklejania logo: {e}")

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
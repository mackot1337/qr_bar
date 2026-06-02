from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.generators import QRCodeGenerator, BarcodeGenerator

app = FastAPI(
    title="QR & Barcode API",
    description="Prototyp API do generowania kodów dla Reacta",
    version="1.0.0"
)

qr_service = QRCodeGenerator()
barcode_service = BarcodeGenerator()

class CodeRequest(BaseModel):
    data: str
    fill_color: str = "black"
    back_color: str = "white"
    barcode_type: str = "code128"

@app.post("/generate/qr")
def generate_qr_endpoint(request: CodeRequest):
    try:
        img_base64 = qr_service.generate(
            data=request.data, 
            fill_color=request.fill_color, 
            back_color=request.back_color
        )
        return {"type": "QR", "image_url": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd generowania QR: {str(e)}")

@app.post("/generate/barcode")
def generate_barcode_endpoint(request: CodeRequest):
    try:
        img_base64 = barcode_service.generate(
            data=request.data, 
            barcode_type=request.barcode_type
        )
        return {"type": "BARCODE", "image_url": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd generowania Barcode: {str(e)}")
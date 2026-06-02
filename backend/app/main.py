from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.generators import QRCodeGenerator, BarcodeGenerator
from app.database import engine, Base, get_db
from app.models import CodeHistory

Base.metadata.create_all(bind=engine)

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
    logo_base64: str = None

@app.post("/generate/qr")
def generate_qr_endpoint(request: CodeRequest, db: Session = Depends(get_db)):
    try:
        img_base64 = qr_service.generate(
            data=request.data, 
            fill_color=request.fill_color, 
            back_color=request.back_color,
            logo_base64=request.logo_base64
        )
        
        db_record = CodeHistory(
            code_type="QR", 
            data=request.data,
            fill_color=request.fill_color,
            back_color=request.back_color
        )
        db.add(db_record)
        db.commit()
        
        return {"type": "QR", "image_url": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd generowania QR: {str(e)}")

@app.post("/generate/barcode")
def generate_barcode_endpoint(request: CodeRequest, db: Session = Depends(get_db)):
    try:
        img_base64 = barcode_service.generate(
            data=request.data, 
            barcode_type=request.barcode_type
        )
        
        db_record = CodeHistory(code_type="BARCODE", data=request.data, barcode_type=request.barcode_type)
        db.add(db_record)
        db.commit()
        
        return {"type": "BARCODE", "image_url": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd generowania Barcode: {str(e)}")
    
@app.get("/history")
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    records = db.query(CodeHistory).order_by(CodeHistory.id.desc()).limit(limit).all()
    return records
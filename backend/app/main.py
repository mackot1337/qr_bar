from enum import Enum
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
from app.generators import QRCodeGenerator, BarcodeGenerator, LogoProcessingException
from app.database import engine, Base, get_db
from app.models import CodeHistory
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QR & Barcode API",
    description="Prototyp API do generowania kodów dla Reacta",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

qr_service = QRCodeGenerator()
barcode_service = BarcodeGenerator()

class BarcodeTypeEnum(str, Enum):
    code128 = "code128"
    code39 = "code39"
    ean13 = "ean13"
    ean8 = "ean8"
    isbn13 = "isbn13"
    upca = "upca"

class CodeRequest(BaseModel):
    data: str = Field(..., min_length=1, max_length=2000, description="Tekst do zakodowania (max 2000 znaków).")
    fill_color: str = Field("black", pattern=r"^([a-zA-Z]+|#[0-9a-fA-F]{3}|#[0-9a-fA-F]{4}|#[0-9a-fA-F]{6}|#[0-9a-fA-F]{8})$")
    back_color: str = Field("white", pattern=r"^([a-zA-Z]+|#[0-9a-fA-F]{3}|#[0-9a-fA-F]{4}|#[0-9a-fA-F]{6}|#[0-9a-fA-F]{8})$")
    barcode_type: BarcodeTypeEnum = BarcodeTypeEnum.code128
    logo_base64: str | None = Field(None, description="Logo w formacie Base64")
    logo_name: str | None = Field(None, description="Nazwa pliku logo")

    @field_validator('logo_base64')
    @classmethod
    def validate_logo_size(cls, v):
        if v and len(v) > 2_000_000: 
            raise ValueError("Przesłane logo jest zbyt duże. Maksymalny rozmiar Base64 to 2MB.")
        return v

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
            back_color=request.back_color,
            image_base64=img_base64,
            logo_base64=request.logo_base64,
            logo_name=request.logo_name
        )
        db.add(db_record)
        db.commit()
        
        return {"type": "QR", "image_url": f"data:image/png;base64,{img_base64}"}
    except LogoProcessingException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Wewnętrzny błąd serwera przy generowaniu QR.")

@app.post("/generate/barcode")
def generate_barcode_endpoint(request: CodeRequest, db: Session = Depends(get_db)):
    try:
        img_base64 = barcode_service.generate(
            data=request.data, 
            barcode_type=request.barcode_type.value,
            fill_color=request.fill_color,
            back_color=request.back_color
        )
        
        db_record = CodeHistory(
            code_type="BARCODE", 
            data=request.data, 
            barcode_type=request.barcode_type.value,
            fill_color=request.fill_color,
            back_color=request.back_color,
            image_base64=img_base64
        )
        db.add(db_record)
        db.commit()
        
        return {"type": "BARCODE", "image_url": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd generowania Barcode: {str(e)}")
    
@app.get("/history")
def get_history(
    skip: int = Query(0, ge=0, description="Liczba pominiętych rekordów"),
    limit: int = Query(10, ge=1, le=100, description="Liczba rekordów (maksymalnie 100)"), 
    db: Session = Depends(get_db)
):
    total_count = db.query(CodeHistory).count()
    records = db.query(CodeHistory).order_by(CodeHistory.id.desc()).offset(skip).limit(limit).all()
    return {
        "total": total_count,
        "items": records
    }
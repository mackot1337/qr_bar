from fastapi import FastAPI

app = FastAPI(
    title="QR & Barcode Generator API",
    description="API do generowania kodów QR i kreskowych",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Backend działa poprawnie!"}
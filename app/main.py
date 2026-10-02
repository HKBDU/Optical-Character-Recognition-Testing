from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.ocr import router as ocr_router

app = FastAPI(title="Pegaxus OCR", version="1.0.0")
app.include_router(health_router)
app.include_router(ocr_router)


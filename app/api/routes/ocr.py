from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.core.config import get_settings
from app.models.request import validate_signature
from app.models.response import OcrAnalysisResponse
from app.services.ocr_pipeline import OcrPipeline

router = APIRouter(prefix="/api/v1/ocr", tags=["ocr"])
pipeline = OcrPipeline()

@router.post("/analyze", response_model=OcrAnalysisResponse)
async def analyze(file: UploadFile = File(...), expectedDocumentType: str | None = Form(None), shipmentId: str | None = Form(None), documentVersionId: str | None = Form(None)) -> OcrAnalysisResponse:
    settings = get_settings()
    limit = settings.max_file_size_mb * 1024 * 1024
    data = await file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, "File exceeds configured size limit")
    if not validate_signature(data, file.content_type, file.filename):
        raise HTTPException(415, "Only valid PDF, PNG and JPEG files are accepted")
    return pipeline.analyze(data, file.filename or "document", expectedDocumentType)


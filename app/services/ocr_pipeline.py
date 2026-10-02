import cv2
import numpy as np
from app.core.config import get_settings
from app.models.response import OcrAnalysisResponse
from app.services.document_classifier import classify
from app.services.extraction_service import extract
from app.services.pdf_service import render_pdf
from app.services.preprocessing_service import variants
from app.services.validation_service import validate

class OcrPipeline:
    def __init__(self):
        self._ocr = None

    def _engine(self):
        if self._ocr is None:
            from app.services.paddle_ocr_service import PaddleOcrService
            s = get_settings()
            self._ocr = PaddleOcrService(s.ocr_lang, s.ocr_use_gpu)
        return self._ocr

    def analyze(self, data: bytes, filename: str, expected: str | None = None) -> OcrAnalysisResponse:
        settings = get_settings()
        try:
            if filename.lower().endswith(".pdf"):
                images = render_pdf(data, settings.ocr_max_pdf_pages)
            else:
                image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                images = [image]
            blocks = []
            engine = self._engine()
            for page, image in enumerate(images, 1):
                page_blocks = []
                for candidate in variants(image):
                    candidate_blocks = engine.recognize(candidate, page)
                    if sum(b.confidence for b in candidate_blocks) > sum(b.confidence for b in page_blocks):
                        page_blocks = candidate_blocks
                blocks.extend(page_blocks)
            kind, type_confidence = classify(blocks, expected)
            fields = extract(blocks)
            overall = round(sum(b.confidence for b in blocks) / len(blocks), 4) if blocks else 0.0
            warnings = validate(fields, type_confidence)
            return OcrAnalysisResponse(success=True, documentType=kind, documentTypeConfidence=type_confidence, overallConfidence=overall, requiresManualReview=bool(warnings) or overall < settings.ocr_medium_confidence or kind == "OTHER", pages=len(images), rawText="\n".join(b.text for b in blocks), blocks=blocks, fields=fields, warnings=warnings)
        except ValueError as exc:
            return OcrAnalysisResponse(success=False, errorCode="INVALID_DOCUMENT", message=str(exc))
        except Exception:
            return OcrAnalysisResponse(success=False, errorCode="OCR_PROCESSING_FAILED", message="OCR processing failed; document remains available for manual review.")


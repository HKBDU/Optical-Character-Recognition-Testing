from app.models.response import OcrBlock
from app.services.document_classifier import classify

def test_classifies_veterinary_certificate():
    blocks = [OcrBlock(text="VETERINARY HEALTH CERTIFICATE", confidence=.98, page=1)]
    assert classify(blocks)[0] == "VETERINARY_HEALTH_CERTIFICATE"

def test_unknown_requires_review():
    assert classify([OcrBlock(text="random text", confidence=.9, page=1)])[0] == "OTHER"


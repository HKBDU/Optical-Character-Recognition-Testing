from app.models.response import OcrBlock

KEYWORDS = {
 "QUARANTINE_CERTIFICATE": ["quarantine certificate", "certificate of quarantine"],
 "VETERINARY_HEALTH_CERTIFICATE": ["veterinary health certificate", "animal health certificate"],
 "IMPORT_PERMIT": ["import permit", "permit to import"],
 "EXPORT_PERMIT": ["export permit", "permit to export"],
 "VACCINATION_RECORD": ["vaccination", "vaccination record", "immunization"],
 "CUSTOMS_DOCUMENT": ["customs declaration", "customs document", "customs"],
 "INVOICE": ["invoice", "invoice number", "amount due"],
 "TRANSPORT_DOCUMENT": ["transport document", "waybill", "consignment"],
}

def classify(blocks: list[OcrBlock], expected: str | None = None) -> tuple[str, float]:
    text = " ".join(b.text.lower() for b in blocks)
    scores = {kind: sum(1 for keyword in words if keyword in text) for kind, words in KEYWORDS.items()}
    kind, hits = max(scores.items(), key=lambda p: p[1], default=("OTHER", 0))
    if hits == 0:
        return "OTHER", 0.0
    confidence = min(0.99, 0.65 + hits * 0.12)
    if expected and expected != kind:
        confidence = min(confidence, 0.55)
    return kind, confidence


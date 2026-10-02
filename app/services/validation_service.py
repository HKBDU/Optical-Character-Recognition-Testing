from app.models.response import ExtractedField
from app.core.config import get_settings

def validate(fields: list[ExtractedField], document_confidence: float) -> list[str]:
    warnings = []
    settings = get_settings()
    if document_confidence < settings.ocr_medium_confidence:
        warnings.append("Document classification confidence is low")
    for f in fields:
        if f.confidence < settings.ocr_medium_confidence:
            warnings.append(f"Low confidence field: {f.name}")
        if f.name in {"issueDate", "expiryDate", "vaccinationDate", "invoiceDate"} and not f.normalizedValue:
            warnings.append(f"Ambiguous or invalid date: {f.name}")
    dates = {f.name: f.normalizedValue for f in fields}
    if dates.get("issueDate") and dates.get("expiryDate") and dates["expiryDate"] < dates["issueDate"]:
        warnings.append("Expiry date is earlier than issue date")
    return warnings


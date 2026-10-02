import re
from app.models.response import ExtractedField, OcrBlock
from app.utils.text import ALIASES, normalize_date

DATE_FIELDS = {"issueDate", "expiryDate", "vaccinationDate", "invoiceDate"}

def _value_after(block: OcrBlock, blocks: list[OcrBlock]):
    match = re.split(r"[:\-]\s*", block.text, maxsplit=1)
    if len(match) == 2 and match[1].strip():
        return match[1].strip(), block
    same = [b for b in blocks if b.page == block.page and b is not block and b.boundingBox and block.boundingBox and min(p[0] for p in b.boundingBox) >= max(p[0] for p in block.boundingBox)]
    if same:
        return min(same, key=lambda b: abs(min(p[1] for p in b.boundingBox)-min(p[1] for p in block.boundingBox))).text.strip(), same[0]
    return None, None

def extract(blocks: list[OcrBlock]) -> list[ExtractedField]:
    fields = []
    for field, aliases in ALIASES.items():
        for block in blocks:
            lower = block.text.lower()
            if not any(alias in lower for alias in aliases):
                continue
            value, source = _value_after(block, blocks)
            if not value:
                continue
            normalized = normalize_date(value) if field in DATE_FIELDS else value.strip()
            confidence = block.confidence * (source.confidence if source else 1.0)
            fields.append(ExtractedField(name=field, value=value, normalizedValue=normalized, confidence=round(confidence, 4), sourceText=block.text, page=block.page, boundingBox=block.boundingBox))
            break
    return fields


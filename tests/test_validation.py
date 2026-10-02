from app.models.response import ExtractedField
from app.services.validation_service import validate

def test_low_confidence_is_flagged():
    warnings = validate([ExtractedField(name="horseName", value="X", confidence=.5)], .9)
    assert any("Low confidence" in item for item in warnings)


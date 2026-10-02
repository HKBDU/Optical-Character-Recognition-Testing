from app.models.response import OcrBlock
from app.services.extraction_service import extract

def test_extracts_fields_and_date():
    blocks = [
        OcrBlock(text="Certificate No: QC-2026-001", confidence=.98, page=1),
        OcrBlock(text="Issue Date: 02 Oct 2026", confidence=.95, page=1),
    ]
    fields = {f.name: f for f in extract(blocks)}
    assert fields["certificateNumber"].value == "QC-2026-001"
    assert fields["issueDate"].normalizedValue == "2026-10-02"

def test_ambiguous_date_is_not_guessed():
    blocks = [OcrBlock(text="Issue Date: 02/03/2026", confidence=.95, page=1)]
    assert extract(blocks)[0].normalizedValue is None


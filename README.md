# Pegaxus OCR Service

Self-hosted OCR microservice for Pegaxus compliance documents. It uses OpenCV, PaddleOCR 3.x, FastAPI and PyMuPDF. No paid/cloud OCR API is used.

## Local run

```powershell
py -3.11 -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

## Docker

```bash
docker build -t pegaxus-ocr .
docker run --rm -p 8001:8000 pegaxus-ocr
```

## API

- `GET /health`
- `POST /api/v1/ocr/analyze` multipart field `file`

```bash
curl -X POST "http://localhost:8001/api/v1/ocr/analyze" -F "file=@samples/quarantine_certificate_sample.txt"
```

The sample text file is only a deterministic fixture; production requests accept PDF, PNG and JPEG. OCR retains text, page, bounding boxes and confidence. OCR never approves or rejects a legal document.

## Configuration

See `.env.example`. Important settings are `MAX_FILE_SIZE_MB`, confidence thresholds, `OCR_LANG` and `OCR_USE_GPU`.

## Tests

```powershell
python -m pytest
```

The separate Pegaxus backend repository is not present in this folder, so EF Core `DocumentVersion` persistence and .NET business matching cannot be generated here. The stable response contract is in `contracts/ocr-response.example.json`.


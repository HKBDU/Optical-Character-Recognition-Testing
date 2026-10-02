from app.models.response import OcrBlock

class PaddleOcrService:
    def __init__(self, lang: str = "en", use_gpu: bool = False):
        from paddleocr import PaddleOCR
        self.engine = PaddleOCR(lang=lang, use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=True, device="gpu:0" if use_gpu else "cpu")

    def recognize(self, image, page: int) -> list[OcrBlock]:
        result = self.engine.predict(image)
        blocks = []
        for item in result:
            data = item.json if hasattr(item, "json") else item
            if callable(data):
                data = data()
            data = data.get("res", data) if isinstance(data, dict) else {}
            texts = data.get("rec_texts", [])
            scores = data.get("rec_scores", [])
            polys = data.get("rec_polys", data.get("dt_polys", []))
            for i, text in enumerate(texts):
                score = float(scores[i]) if i < len(scores) else 0.0
                poly = polys[i].tolist() if i < len(polys) and hasattr(polys[i], "tolist") else (polys[i] if i < len(polys) else [])
                blocks.append(OcrBlock(text=str(text), confidence=max(0, min(1, score)), page=page, boundingBox=poly))
        return blocks


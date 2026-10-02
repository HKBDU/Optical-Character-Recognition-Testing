import fitz
import numpy as np

def render_pdf(data: bytes, max_pages: int) -> list[np.ndarray]:
    doc = fitz.open(stream=data, filetype="pdf")
    try:
        if len(doc) > max_pages:
            raise ValueError(f"PDF exceeds maximum page count of {max_pages}")
        pages = []
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            pages.append(np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n))
        return pages
    finally:
        doc.close()


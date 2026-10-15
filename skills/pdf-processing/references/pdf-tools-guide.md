# PDF Processing Tools & Library Comparison

## Python Ecosystem Overview

| Library | Primary Use Case | Strengths | Limitations |
| :--- | :--- | :--- | :--- |
| **`pypdf`** | General page manipulation, text extraction, encryption, metadata | Pure Python, lightweight, fast, no external system binaries required | Basic table extraction only; no OCR |
| **`pdfplumber`** | Precision text & table extraction | Visual inspection of lines/boxes, highly configurable table parsing | Slower than pypdf; memory heavy on large PDFs |
| **`reportlab`** | PDF generation from scratch | Highly flexible, flowable layouts, complex styling and charts | Steep learning curve; cannot edit existing PDFs |
| **`ocrmypdf`** | OCR for scanned PDFs | Adds searchable text layer beneath original scanned images | Requires Tesseract, Ghostscript, and Poppler installed |
| **`pypdfium2`** / `pdf2image` | Rendering PDF pages to images (PNG/JPEG) | Extremely fast rendering based on Google PDFium; great for visual audits | Image output only; no PDF editing |

---

## Command-Line System Tools

When available in the host environment:

### `pdftotext` (Poppler Utilities)
Fastest way to extract layout-preserved plain text from the command line:
```bash
pdftotext -layout input.pdf output.txt
```

### `pdfimages` (Poppler Utilities)
Extract all embedded images from a PDF in their native formats (JPEG, PNG):
```bash
pdfimages -png input.pdf extracted_img_prefix
```

### `ocrmypdf`
Add a clean OCR text layer to a scanned PDF without rasterizing existing vector graphics:
```bash
ocrmypdf --deskew --clean scanned_input.pdf searchable_output.pdf
```

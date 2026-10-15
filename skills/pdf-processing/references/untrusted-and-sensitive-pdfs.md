# Untrusted PDFs, Redaction, Encryption, Forms, Licensing

Library behavior checked against pypdf 6.x and PyPI metadata in October 2026. Verify method names against the installed version.

## Untrusted input guardrails

- Check size before parsing (`os.path.getsize`), refuse files above a limit that fits your use case, and cap `len(reader.pages)`.
- Run extraction in a subprocess with a timeout and memory limit when handling files from strangers; a malformed PDF can hang or exhaust memory.
- Never open attachments or execute embedded JavaScript/launch actions found in a PDF; libraries here only parse, they do not run them.
- Keep `pypdf`, `pdfplumber`, and `pypdfium2` current; parser fixes are frequent.
- Write outputs to a new path in a new directory; do not trust filenames from the PDF.

## Redaction: what works and what does not

Drawing a filled rectangle (ReportLab overlay, annotation, image stamp) only hides text visually. The text, metadata, bookmarks, form values, and embedded files remain.

Reliable approaches:
1. Use a tool with a real redaction feature that removes the content (for example PyMuPDF's redaction API, which is AGPL-licensed, or a commercial/offline tool). Check the license before use in a product.
2. Rasterize each page to an image after drawing the boxes, then rebuild the PDF from images (and OCR if searchability is needed). This destroys the text layer but also quality and accessibility.

Always verify: extract text from the output (`pdftotext -layout out.pdf -`) and search for the redacted strings; check `reader.metadata`, attachments, and form fields. Redaction of personal or legal material needs a human sign-off.

## Metadata hygiene

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("in.pdf")
writer = PdfWriter(clone_from=reader)
writer.add_metadata({"/Title": "Public report"})  # overrides listed keys only
with open("out.pdf", "wb") as f:
    writer.write(f)
```

Setting keys does not remove XMP metadata or other hidden data; inspect the result (`reader.xmp_metadata`) and use a sanitizing tool for strict needs.

## Encryption and decryption

```python
import getpass
from pypdf import PdfReader, PdfWriter

writer = PdfWriter(clone_from="in.pdf")
writer.encrypt(user_password=getpass.getpass("Password: "), algorithm="AES-256")
with open("encrypted.pdf", "wb") as f:
    writer.write(f)

reader = PdfReader("encrypted.pdf")
if reader.is_encrypted:
    reader.decrypt(getpass.getpass("Password: "))
```

AES algorithms require the `cryptography` package. Never hard-code passwords, put them in command lines, or log them. Do not attempt to crack or bypass passwords; ask the user for the password or an unprotected copy.

## Filling AcroForm fields

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
print(reader.get_fields())            # discover field names and types
writer = PdfWriter(clone_from=reader)
writer.update_page_form_field_values(
    writer.pages[0], {"full_name": "Ada Lovelace"}, auto_regenerate=False
)
writer.set_need_appearances_writer(True)  # ask viewers to regenerate field appearance
with open("filled.pdf", "wb") as f:
    writer.write(f)
```

Checkboxes and radio buttons use export values specific to the form; read them from `get_fields()`. XFA forms are not supported by these libraries. Verify the result by rendering with a different viewer, because appearance streams differ across viewers.

## OCR notes

`ocrmypdf` needs Tesseract and Ghostscript installed. Useful options: `--skip-text` (OCR only pages lacking text, good for mixed documents), `--force-ocr` (rasterize and OCR everything), `-l eng+deu` (languages), `--deskew`, and `--clean` (requires `unpaper`). OCR runs locally; do not send sensitive scans to a cloud OCR service without the user's approval.

## Licensing note

pypdf (BSD-3), pdfplumber (MIT), pypdfium2 (BSD-3/Apache-2.0 with bundled PDFium licenses), reportlab (BSD-style), ocrmypdf (MPL-2.0). PyMuPDF is dual-licensed AGPL/commercial; do not add it to closed-source software without checking the terms.

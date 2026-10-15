# PDF Quality & Verification Checklist

Follow this checklist whenever modifying, generating, or extracting data from PDF documents.

## 1. Text Extraction Verification
- [ ] Check for replacement characters (`` or `?`) indicating unsupported font encodings.
- [ ] Verify ligature resolution (ensure "fi", "fl", "ff" are not silently dropped or split).
- [ ] Confirm reading order in multi-column documents (ensure right column does not interleave with left column lines).

## 2. Table Extraction Verification
- [ ] Verify row count matches visual inspection.
- [ ] Check for header row alignment (ensure headers are not absorbed as data rows).
- [ ] Verify negative numbers, currency symbols, and decimals are preserved accurately.
- [ ] Confirm multi-line cell entries are merged properly within their respective cells.

## 3. Visual Layout Verification
When generating new PDFs:
- [ ] Page margins: Ensure text does not touch or exceed printable margins (minimum 0.5 in / 36 pt).
- [ ] Page breaks: Headings must not be orphaned at the bottom of a page without at least 2 lines of following body text (widow/orphan control).
- [ ] Fonts: Ensure standard base fonts (Helvetica, Times, Courier) or embedded TTF/OTF fonts are used so the document renders identically on all client OSes.

---
name: docx-processing
description: >
  Generate, parse, modify, and format Microsoft Word (.docx) documents
  programmatically. Use when creating styled corporate reports, extracting text
  and tables from Word documents with python-docx, manipulating document sections,
  headers, footers, and page breaks, or inspecting OpenXML document structures.
compatibility: >
  Agent Skills-compatible coding agents operating with Python docx manipulation
  libraries (python-docx).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "docx, word, office, python-docx, document-processing, formatting"
  topics: "office, documentation, devtools"
---

# Programmatic Microsoft Word (.docx) Processing

Microsoft Word documents (`.docx`) are zipped OpenXML packages containing structured XML parts representing document body, styles, headers, footers, relationships, and embedded media. This skill provides a complete, repeatable workflow for creating, reading, and modifying `.docx` files programmatically while preserving proper formatting, typographic hierarchy, and structural integrity.

Detailed reference guides:
- [OpenXML Structure & python-docx Internals](references/docx-structure.md)

---

## The 6-Step Document Engineering Workflow

1. **Inspect & Clarify Requirements**: Identify required margins, orientation (Portrait/Landscape), fonts, headers, footers, and branding color palettes.
2. **Select Tooling**: Use `python-docx` for Python workflows. Avoid shell tools that convert to plaintext and lose structure.
3. **Draft / Modify Document**: Build document linearly using semantic styles (`Heading 1`, `Heading 2`, `Normal`, `Table Grid`).
4. **Validate Document Structure**: Confirm that paragraph runs, table cells, and page breaks are valid OpenXML nodes without corruption.
5. **Inspect Content & Formatting**: Verify column widths, text wrapping, table alignments, and header/footer bindings.
6. **Deliver Genuine Output Artifact**: Ensure the final output is a genuine `.docx` file (never a renamed HTML or text file).

---

## 1. Creating a Styled Word Document with `python-docx`

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def generate_report(output_path: str):
    doc = Document()

    # Configure Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Header & Footer
    header = doc.sections[0].header
    header_p = header.paragraphs[0]
    header_p.text = "Confidential - Internal Engineering Review"
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    footer = doc.sections[0].footer
    footer_p = footer.paragraphs[0]
    footer_p.text = "Acme Corp © 2026"
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Document Title (Heading 0 / Title)
    title = doc.add_heading("Architecture Assessment Report", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Lead Paragraph with styled runs
    lead = doc.add_paragraph()
    run_bold = lead.add_run("Executive Summary: ")
    run_bold.bold = True
    lead.add_run(
        "This document details the transition from monolithic storage to "
        "distributed object stores across all production regions."
    )

    # Section Heading
    doc.add_heading("1. Throughput Benchmarks", level=1)

    # Adding a Structured Table
    data = [
        ["Service Tier", "Requests / Sec", "p99 Latency (ms)", "Status"],
        ["Database Layer", "14,500", "4.2", "OPTIMAL"],
        ["API Gateway", "52,000", "12.8", "OPTIMAL"],
        ["Async Queue", "8,200", "45.0", "ATTENTION"],
    ]

    table = doc.add_table(rows=len(data), cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            # Format header row
            if r_idx == 0:
                p = cell.paragraphs[0]
                for run in p.runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # Add Page Break before next major chapter
    doc.add_page_break()

    doc.add_heading("2. Migration Timeline", level=1)
    p2 = doc.add_paragraph("Target completion is Q4 2026.")

    # Save artifact
    doc.save(output_path)
    print(f"Document saved successfully: {output_path}")

if __name__ == "__main__":
    generate_report("architecture_review.docx")
```

---

## 2. Reading and Modifying Existing `.docx` Files

```python
from docx import Document

def inspect_and_update_docx(file_path: str, target_author: str):
    doc = Document(file_path)

    # Extract all text paragraphs
    full_text = [p.text for p in doc.paragraphs if p.text.strip()]
    print(f"Total paragraphs: {len(full_text)}")

    # Modify specific placeholder text in place
    for p in doc.paragraphs:
        if "{{AUTHOR}}" in p.text:
            p.text = p.text.replace("{{AUTHOR}}", target_author)

    # Read tables
    for t_idx, table in enumerate(doc.tables):
        print(f"Table {t_idx}: {len(table.rows)} rows x {len(table.columns)} cols")

    # Save to new file (never overwrite input directly)
    doc.save("updated_document.docx")
```

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| Writing HTML and saving with `.docx` extension | Microsoft Word reports corrupt file error on open | Generate genuine OpenXML zip package via `python-docx` |
| Overwriting source file while open in Word | Permission denied crash (`EBUSY` / `PermissionError`) | Write to separate destination file |
| Manual spacing with multiple empty paragraphs | Inconsistent layout across different page sizes and printers | Use `paragraph.paragraph_format.space_after = Pt(12)` |
| Hardcoding non-standard fonts | Missing font falls back to Times New Roman on recipient machine | Use standard cross-platform fonts (Calibri, Arial, Georgia) |

---

## 4. Verification Checklist

- [ ] Output is a genuine `.docx` zip package (verified via `zipfile.is_zipfile(path)`).
- [ ] Heading hierarchy follows H1 -> H2 -> H3 without skipping.
- [ ] Tables have proper borders, cell padding, and header row formatting.
- [ ] Document margins, headers, and footers are consistently configured.
- [ ] File opens in Word or LibreOffice Writer without repair warnings.

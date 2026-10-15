# OpenXML Structure & python-docx Internals

A `.docx` file is a ZIP archive adhering to the ISO/IEC 29500 OpenXML standard.

## 1. Internal Archive Anatomy

Renaming `document.docx` to `document.zip` and unzipping reveals:
```text
document/
├── [Content_Types].xml        # MIME type mappings for parts
├── _rels/                    # Package-level relationships
│   └── .rels
└── word/
    ├── document.xml          # Core body text, paragraphs, tables
    ├── styles.xml            # Predefined character and paragraph styles
    ├── header1.xml           # Running headers
    ├── footer1.xml           # Running footers
    ├── settings.xml          # Document-level properties and compatibility
    ├── media/                # Embedded PNG, JPEG, SVG images
    └── _rels/
        └── document.xml.rels # Hyperlinks, image targets, style relationships
```

---

## 2. Paragraphs vs Runs

In OpenXML:
- A **Paragraph (`<w:p>`)** represents a block of text separated by a newline. It contains paragraph-level properties (alignment, spacing before/after, indent).
- A **Run (`<w:r>`)** represents a contiguous string of text with identical formatting (font, size, bold, italic, color). A single paragraph usually contains multiple runs.

```python
# To change formatting of a single word in python-docx:
p = doc.add_paragraph("This is ")
p.add_run("bold").bold = True
p.add_run(" and this is ")
p.add_run("italic.").italic = True
```

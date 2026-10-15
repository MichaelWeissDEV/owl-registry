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

---

## 3. Parts worth inspecting (read-only)

| Part | Why look |
| :--- | :--- |
| `word/document.xml` | Body text; `<w:ins>`/`<w:del>` mark tracked changes (python-docx ignores them when reading text in some cases; verify) |
| `word/comments.xml` | Review comments with author names |
| `word/_rels/document.xml.rels` | External hyperlinks, images, remote templates (`TargetMode="External"`) |
| `word/settings.xml` | `attachedTemplate`, compatibility mode, track-revisions flag |
| `docProps/core.xml`, `docProps/app.xml` | Author, last modified by, timestamps, application |
| `word/vbaProject.bin` | Macros (should not exist in a `.docx`; present in `.docm`) |

List parts without extracting: `python3 -I -c "import zipfile,sys; print(*zipfile.ZipFile(sys.argv[1]).namelist(), sep='\n')" file.docx`. Do not extract archives from untrusted sources into a directory that contains scripts; extract into a fresh empty directory and cap sizes.

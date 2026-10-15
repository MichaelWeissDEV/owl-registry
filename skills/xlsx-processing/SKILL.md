---
name: xlsx-processing
description: >
  Create, parse, format, and audit Microsoft Excel (.xlsx) workbooks programmatically
  using openpyxl. Use when generating financial spreadsheets with calculated
  formulas, applying cell styles and number formats, managing multiple worksheets,
  building structured tables and charts, or validating formula integrity.
compatibility: >
  Agent Skills-compatible coding agents operating with Python Excel manipulation
  libraries (openpyxl).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "xlsx, excel, openpyxl, spreadsheets, formulas, financial-modeling, office"
  topics: "office, documentation, devtools"
---

# Programmatic Microsoft Excel (.xlsx) Processing

Excel workbooks (`.xlsx`) represent structured tabular data, multi-sheet workbooks, formula calculation trees, cell styling, and data formatting. Building production-grade Excel files requires disciplined separation of raw numeric data from display formatting, precise formula syntax, and validation of cell coordinates.

Detailed reference guides:
- [openpyxl Patterns, Formulas & Formatting Guide](references/openpyxl-guide.md)

---

## The 6-Step Spreadsheet Engineering Workflow

1. **Inspect Requirements**: Determine required sheets, data schemas, formula relationships (`SUM`, `AVERAGE`, `VLOOKUP`), and number formatting (currency, percentages, dates).
2. **Select Tooling**: Use `openpyxl` for Python `.xlsx` generation and modification.
3. **Draft / Update Workbook**: Write raw typed data (integers, floats, dates, strings) into cells—never format numbers as pre-rendered text strings like `"$1,200.00"`.
4. **Apply Number Formatting & Styles**: Set explicit `number_format`, font weights, header fills, column widths, and cell borders.
5. **Validate Calculation Formulas**: Confirm formula syntax uses uppercase names, valid coordinate ranges, and produces no `#VALUE!` or `#REF!` errors.
6. **Save & Distribute Clean Artifact**: Save to a genuine `.xlsx` file and verify readability.

---

## 1. Creating a Styled Financial Model with `openpyxl`

```python
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_financial_model(output_path: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Q4 Financials"

    # Styling Palettes
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    total_font = Font(name="Calibri", size=11, bold=True)
    border_thin = Side(border_style="thin", color="D9D9D9")
    cell_border = Border(top=border_thin, left=border_thin, right=border_thin, bottom=border_thin)
    double_bottom = Border(bottom=Side(border_style="double", color="000000"), top=border_thin)

    # 1. Document Title
    ws["A1"] = "Acme Corp - Q4 Performance Summary"
    ws["A1"].font = Font(name="Calibri", size=16, bold=True)
    ws["A2"] = f"Report Date: {date.today().isoformat()}"
    ws["A2"].font = Font(name="Calibri", size=10, italic=True)

    # 2. Table Headers
    headers = ["Department", "Budget", "Actual Spend", "Variance", "% Utilized"]
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center" if col_idx > 1 else "left")

    # 3. Data Rows
    departments = [
        ("Engineering", 250000, 241200),
        ("Product & Design", 80000, 78500),
        ("Sales & Marketing", 140000, 149300),
        ("Operations & HR", 65000, 61000),
    ]

    start_row = 5
    for i, (dept, budget, actual) in enumerate(departments):
        r = start_row + i
        ws.cell(row=r, column=1, value=dept).border = cell_border
        
        # Numeric values stored as raw numbers (NOT strings)
        c_budget = ws.cell(row=r, column=2, value=budget)
        c_budget.number_format = "$#,##0"
        c_budget.border = cell_border

        c_actual = ws.cell(row=r, column=3, value=actual)
        c_actual.number_format = "$#,##0"
        c_actual.border = cell_border

        # Formula: Budget - Actual
        c_var = ws.cell(row=r, column=4, value=f"=B{r}-C{r}")
        c_var.number_format = "$#,##0"
        c_var.border = cell_border

        # Formula: Actual / Budget
        c_pct = ws.cell(row=r, column=5, value=f"=C{r}/B{r}")
        c_pct.number_format = "0.0%"
        c_pct.border = cell_border

    # 4. Total Summary Row
    total_row = start_row + len(departments)
    ws.cell(row=total_row, column=1, value="Total").font = total_font
    ws.cell(row=total_row, column=1).border = double_bottom

    c_tot_b = ws.cell(row=total_row, column=2, value=f"=SUM(B{start_row}:B{total_row-1})")
    c_tot_b.font = total_font
    c_tot_b.number_format = "$#,##0"
    c_tot_b.border = double_bottom

    c_tot_a = ws.cell(row=total_row, column=3, value=f"=SUM(C{start_row}:C{total_row-1})")
    c_tot_a.font = total_font
    c_tot_a.number_format = "$#,##0"
    c_tot_a.border = double_bottom

    c_tot_v = ws.cell(row=total_row, column=4, value=f"=B{total_row}-C{total_row}")
    c_tot_v.font = total_font
    c_tot_v.number_format = "$#,##0"
    c_tot_v.border = double_bottom

    c_tot_p = ws.cell(row=total_row, column=5, value=f"=C{total_row}/B{total_row}")
    c_tot_p.font = total_font
    c_tot_p.number_format = "0.0%"
    c_tot_p.border = double_bottom

    # 5. Auto-fit Column Widths with comfortable padding
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(output_path)
    print(f"Spreadsheet successfully generated: {output_path}")

if __name__ == "__main__":
    generate_financial_model("q4_financials.xlsx")
```

---

## 2. Reading Formulas vs Cached Values

When opening workbooks created by third parties:
- `load_workbook(filename)`: Reads the **formula text** (`=SUM(A1:A10)`).
- `load_workbook(filename, data_only=True)`: Reads the **cached evaluated value** (`150.0`).
*(Note: If a formula was generated by a script and never opened in Excel, `data_only=True` will return `None` because openpyxl does not evaluate formula engines.)*

```python
from openpyxl import load_workbook

# Read formula text
wb_formulas = load_workbook("q4_financials.xlsx", data_only=False)
print("Formula:", wb_formulas["Q4 Financials"]["B9"].value) # Output: =SUM(B5:B8)

# Read evaluated values
wb_values = load_workbook("q4_financials.xlsx", data_only=True)
print("Cached Value:", wb_values["Q4 Financials"]["B9"].value)
```

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| Writing numbers formatted as strings: `"$500"` | Breaks Excel mathematical formulas (`#VALUE!`) | Store raw number `500`, set `number_format = "$#,##0"` |
| Lowercase formula names: `=sum(a1:a5)` | Compatibility errors in non-English Excel versions | Always use uppercase: `=SUM(A1:A5)` |
| Overwriting open workbooks | File lock crash on Windows (`PermissionError`) | Save to new file or ensure workbook is closed |
| Relying on `data_only=True` for newly created files | Returns `None` because openpyxl has no calculation engine | Open in Excel/LibreOffice to calculate caches |

---

## 4. Verification Checklist

- [ ] All numeric and financial cells contain raw numeric types (not pre-formatted strings).
- [ ] Number formats explicitly set (`$#,##0`, `0.0%`, `YYYY-MM-DD`).
- [ ] Formula names in uppercase (`SUM`, `AVERAGE`, `IF`, `VLOOKUP`).
- [ ] Column widths adjusted to prevent `###` overflow truncation.
- [ ] File verified with `zipfile.is_zipfile(path)` and opens without error.

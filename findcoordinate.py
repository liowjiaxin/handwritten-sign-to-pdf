import fitz  # PyMuPDF

pdf_path = "dangerous_goods_form.pdf"

doc = fitz.open(pdf_path)

print("=== Form Field Coordinates ===\n")

for page_index, page in enumerate(doc):
    widgets = page.widgets()
    if not widgets:
        continue

    print(f"--- Page {page_index + 1} ---")
    for w in widgets:
        print("Field Name:", w.field_name)
        print("Field Type:", w.field_type_string)
        print("Rect:", w.rect)  # <-- Coordinates (x0, y0, x1, y1)
        print("Width:", w.rect.width)
        print("Height:", w.rect.height)
        print()

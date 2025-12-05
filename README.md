# 🖊️ Signature Extraction and PDF Signing

This project provides a simple, automated solution to extract a handwritten signature from an image and seamlessly place it onto a PDF form at the bottom-right corner. The extracted signature is automatically processed to have a transparent background and is scaled to fit neatly on the page.

---

## ✨ Features

* Extract signature from scanned images (`.jpg`, `.png`).
* Automatically create a transparent PNG signature file.
* Insert the signature into a PDF form using PyMuPDF (`fitz`).
* Auto-scale the signature to fit within defined maximum width and height.
* Automatically places the signature at the bottom-right corner of the PDF's first page with a configurable margin.
* Saves a new PDF with the signature applied.

---

## 🛠️ Requirements

* Python 3.10+ (tested with 3.14)

### Dependencies

Install the required Python libraries:

```bash
pip install opencv-python numpy pymupdf
```

**Windows Note:** If your Python path contains spaces (e.g., `C:/Users/Liow Jia Xin/...`), use quotes and `&` in PowerShell:

```powershell
& "C:/Users/Liow Jia Xin/AppData/Local/Python/bin/python.exe" -m pip install opencv-python numpy pymupdf
```

---

## 🚀 Setup & Usage

1. Place the following files in the same folder:

   * `sign.jpg` → Your scanned signature image
   * `dangerous_goods_form.pdf` → The PDF form to sign

2. Update Parameters (Optional):

   You can modify `MAX_SIG_WIDTH`, `MAX_SIG_HEIGHT`, or `MARGIN` in the script to adjust signature size or margin.

3. Run the script:

```bash
python signtopdf.py
```

### Output Files

* `my_signature_transparent.png` → Extracted transparent signature image
* `signed_dangerous_goods_form.pdf` → PDF with your signature applied

---

## 🖼️ Visual Walkthrough

1. **Input Image:** Your scanned or photographed signature. Background is removed automatically.
2. **Transparent Signature:** The extracted signature with a transparent background.
3. **Signed PDF:** Final document with the scaled, transparent signature at the bottom-right corner.

---

## 🧠 How It Works

### Signature Extraction

* Converts input image to grayscale.
* Applies Gaussian blur to reduce noise.
* Uses adaptive thresholding to separate the dark signature from the light background.
* Cleans small artifacts using morphology operations.
* Creates a transparent PNG using the thresholded mask as the alpha channel.

### PDF Signing

* Opens the target PDF with PyMuPDF (`fitz`).
* Computes scaled size while maintaining aspect ratio (`MAX_SIG_WIDTH` & `MAX_SIG_HEIGHT`).
* Calculates bottom-right coordinates based on page size and `MARGIN`.
* Inserts the signature onto the first page.
* Saves the signed PDF.

---

## ⚙️ Customization

* **Change Placement:** Adjust `MARGIN` or manually set coordinates for specific positions.
* **Multiple Pages:** Loop through `doc.pages()` to sign every page.
* **Multiple Signatures:** Use OpenCV or PyMuPDF to detect signature boxes and automatically place signatures for multiple signers.

---

### Example Configuration

```python
SIGN_IMAGE = "sign.jpg"
PDF_TEMPLATE = "dangerous_goods_form.pdf"
OUTPUT_PDF = "signed_form.pdf"
MAX_SIG_WIDTH = 200   # Maximum width in pixels
MAX_SIG_HEIGHT = 100  # Maximum height in pixels
MARGIN = 50           # Margin from right and bottom edges in pixels
```

After running with this configuration, `signed_form.pdf` will have your signature visible on the bottom-right corner of the first page.

---

## 🛠️ Tips & Troubleshooting

1. **Signature Not Appearing:**

   * Ensure `my_signature_transparent.png` was successfully generated.
   * Check that the signature is placed within the PDF page boundaries. Adjust `MAX_SIG_WIDTH`, `MAX_SIG_HEIGHT`, or `MARGIN` if needed.

2. **Python Path Issues (Windows):**

   * Use quotes and `&` when executing Python or pip if your path contains spaces.

3. **Missing Libraries:**

   * Install libraries using:

     ```bash
     pip install opencv-python numpy pymupdf
     ```

4. **Incorrect Scaling:**

   * Modify `MAX_SIG_WIDTH` and `MAX_SIG_HEIGHT` to better fit your PDF.
   * Aspect ratio is preserved, so only one dimension might hit the maximum.

5. **Multiple Pages:**

   * To sign all pages, loop through `doc.pages()` and apply the same placement logic.

6. **File Names & Locations:**

   * Ensure `SIGN_IMAGE` and `PDF_TEMPLATE` paths are correct relative to the script location.

---

✅ This README provides all information needed to extract a signature from an image and automatically place it on a PDF form with transparency and scaling.

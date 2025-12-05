import cv2
import numpy as np
import fitz  # PyMuPDF

# ---------------- CONFIG ----------------
SIGN_IMAGE = "sign.jpg"
TRANSPARENT_SIG = "my_signature_transparent.png"
PDF_TEMPLATE = "dangerous_goods_form.pdf"
OUTPUT_PDF = "signed_dangerous_goods_form.pdf"

# Max signature size in PDF points
MAX_SIG_WIDTH = 200
MAX_SIG_HEIGHT = 100
MARGIN = 50  # margin from page edges
# ----------------------------------------

def extract_signature(input_path, output_path):
    """Extract signature from an image and make background transparent."""
    img = cv2.imread(input_path)
    if img is None:
        print("Error loading image!")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Adaptive threshold: signature becomes white, background black
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        15, 8
    )

    # Clean small artifacts
    kernel = np.ones((3,3), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Create RGBA with alpha = signature mask
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = clean

    cv2.imwrite(output_path, rgba)
    print(f"✅ Transparent signature saved: {output_path}")
    return rgba

def insert_signature_to_pdf(pdf_template, signature_file, output_pdf, max_width, max_height, margin):
    """Insert signature onto PDF bottom-right corner with auto-scaling."""
    doc = fitz.open(pdf_template)
    page = doc[0]  # first page

    sig_img = fitz.Pixmap(signature_file)

    # Compute scale to fit max width/height
    scale_w = max_width / sig_img.width
    scale_h = max_height / sig_img.height
    scale = min(scale_w, scale_h, 1.0)  # do not enlarge

    sig_w = int(sig_img.width * scale)
    sig_h = int(sig_img.height * scale)

    # Bottom-right placement with margin
    page_width, page_height = page.rect.width, page.rect.height
    x0 = page_width - sig_w - margin
    y0 = page_height - sig_h - margin

    rect = fitz.Rect(x0, y0, x0 + sig_w, y0 + sig_h)
    page.insert_image(rect, filename=signature_file)

    doc.save(output_pdf)
    doc.close()
    print(f"✅ Signed PDF saved: {output_pdf}")

# ---------------- MAIN ----------------
extract_signature(SIGN_IMAGE, TRANSPARENT_SIG)
insert_signature_to_pdf(PDF_TEMPLATE, TRANSPARENT_SIG, OUTPUT_PDF, MAX_SIG_WIDTH, MAX_SIG_HEIGHT, MARGIN)

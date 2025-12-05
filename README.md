🖊️ Signature Extraction and PDF Signing

This project provides a simple, automated solution to extract a handwritten signature from an image and seamlessly place it onto a PDF form at the bottom-right corner. The extracted signature is automatically processed to have a transparent background and is scaled to fit neatly on the page.

✨ Features

Extract signature from scanned images (.jpg, .png).

Automatically create a transparent background PNG signature file.

Insert the signature into a PDF form using PyMuPDF (fitz).

Auto-scale the signature to fit within defined maximum width and height.

Automatically places the signature at the bottom-right corner of the PDF's first page with a configurable margin.

Saves a new PDF with the signature applied.

🛠️ Requirements

Python 3.10+ (tested with 3.14)

Dependencies

Install the required Python libraries using pip:

pip install opencv-python numpy pymupdf


Note for Windows Users: If your Python path contains spaces (e.g., C:/Users/Liow Jia Xin/...), use quotes and & in PowerShell to run the command:

& "C:/Users/Liow Jia Xin/AppData/Local/Python/bin/python.exe" -m pip install opencv-python numpy pymupdf


🚀 Setup & Usage

Place the files in the same folder:

sign.jpg → Your scanned signature image.

dangerous_goods_form.pdf → The PDF form you need to sign.

Update Parameters (Optional):

You can modify MAX_SIG_WIDTH, MAX_SIG_HEIGHT, or MARGIN within the script if you need to adjust the maximum signature size or its distance from the page edges.

Run the script:

python signtopdf.py


Or, on Windows PowerShell (adjust path as needed):

& "C:/Users/Liow Jia Xin/AppData/Local/Python/bin/python.exe" "C:/Users/Liow Jia Xin/Downloads/signtopdf.py"


Output Files

After running the script, the following files will be generated in the same directory:

my_signature_transparent.png → The extracted transparent signature image.

signed_dangerous_goods_form.pdf → The new PDF with your signature applied.

🖼️ Visual Walkthrough

This section illustrates the process from input image to the final signed document.

1. Input Image

Your scanned or photographed signature. The quality of the background does not matter, as it will be removed.

2. Transparent Signature

The extracted signature with a perfectly transparent background, ready to be placed on any document.

3. Signed PDF

The final document with the transparent, scaled signature placed neatly in the bottom-right corner.

🧠 How It Works

Signature Extraction

The script uses OpenCV to robustly separate the handwriting from the background:

Converts the input image to grayscale.

Applies a Gaussian blur to effectively reduce noise.

Uses adaptive thresholding to create a binary mask, cleanly separating the dark signature from the light background.

Cleans small artifacts (speckles) using morphology operations.

Creates a transparent PNG by using the thresholded mask as the alpha channel (transparency layer).

PDF Signing

The script uses PyMuPDF (fitz) for PDF manipulation:

Opens the target PDF document.

Computes the scaled size of the signature while maintaining its aspect ratio, ensuring it fits within MAX_SIG_WIDTH and MAX_SIG_HEIGHT.

Calculates the bottom-right corner coordinates based on the page size and the configured MARGIN.

Inserts the scaled, transparent signature image onto the first page.

Saves the document as a new, signed PDF.

⚙️ Customization

The script is easy to adapt for different use cases:

Change Placement: Adjust the MARGIN variable, or calculate and manually set the coordinates for specific positioning.

Multiple Pages: Loop through doc.pages() to apply the signature to every page of the document.

Multiple Signatures: Use OpenCV or PyMuPDF's annotation detection features to find signature boxes and automate placement for multiple signers.

Example Configuration

SIGN_IMAGE = "sign.jpg"
PDF_TEMPLATE = "dangerous_goods_form.pdf"
OUTPUT_PDF = "signed_form.pdf"
MAX_SIG_WIDTH = 200 # Maximum width in pixels
MAX_SIG_HEIGHT = 100 # Maximum height in pixels
MARGIN = 50 # Margin from right and bottom edges in pixels


After running with this configuration, signed_form.pdf will have your signature visible on the bottom-right corner of the first page.
import cv2
import numpy as np

def extract_signature(input_path, output_path):
    # --- 1. LOAD IMAGE ---
    img = cv2.imread(input_path)
    if img is None:
        print("Error loading image!")
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 2. REMOVE NOISE ---
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # --- 3. THRESHOLD TO EXTRACT INK ---
    # Converts the signature to WHITE and background to BLACK
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        15, 8
    )

    # --- 4. CLEAN THRESHOLD ---
    kernel = np.ones((3,3), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # --- 5. CREATE TRANSPARENT BACKGROUND ---
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Where signature is black (255 in 'clean'), set alpha to 255
    # Where background is white (0 in 'clean'), set alpha to 0
    rgba[:, :, 3] = clean

    # --- 6. SAVE ---
    cv2.imwrite(output_path, rgba)
    print("Transparent signature saved:", output_path)

    return img, rgba

def blend_transparent_image(foreground_rgba, background_color=(0, 0, 255)):
    """
    Blends the transparent RGBA foreground onto a solid color background.
    """
    if foreground_rgba is None:
        return None

    (h, w) = foreground_rgba.shape[:2]

    # Create a solid background image (BGR)
    background = np.full((h, w, 3), background_color, dtype=np.uint8)

    # Extract alpha channel
    alpha = foreground_rgba[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    # Convert colors to float
    fg_colors = foreground_rgba[:, :, 0:3].astype(float)
    bg_colors = background.astype(float)

    # Blend
    for c in range(0, 3):
        bg_colors[:, :, c] = (fg_colors[:, :, c] * alpha) + (bg_colors[:, :, c] * alpha_inv)

    return bg_colors.astype(np.uint8)

def resize_for_display(image, max_width=800, max_height=600):
    h, w = image.shape[:2]
    scale = min(max_width/w, max_height/h)
    if scale < 1:
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h))
    return image

INPUT_FILE = "sign.jpg"
OUTPUT_FILE = "my_signature_transparent.png"

original, transparent = extract_signature(INPUT_FILE, OUTPUT_FILE)

if original is not None:
    blended = blend_transparent_image(transparent, background_color=(0,0,255))
    blended_resized_original = resize_for_display(original)
    cv2.imshow("Original", blended_resized_original)
    
    blended_resized = resize_for_display(blended)
    cv2.imshow("Signature on Red (Resized)", blended_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


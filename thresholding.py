import cv2
import numpy as np
from pathlib import Path

def create_color_bounding_box(
    image_path,
    lower_hsv=None,
    upper_hsv=None,
    min_area=120,
    min_dimension=8,
    kernel_size=3,
    open_iters=0,
    close_iters=1,
    enhance_dark=True,
    clahe_clip=2.0,
):
    """
    Creates a rectangular bounding box around a given color using HSV thresholding.
    
    Args:
        image_path (str): Path to the image file
        lower_hsv (tuple): Lower HSV bounds (default: red lower bound)
        upper_hsv (tuple): Upper HSV bounds (default: red upper bound)
        min_area (int): Minimum contour area to keep as a bounding box
        min_dimension (int): Minimum width/height (px) for a kept box
        kernel_size (int): Kernel size used for morphology cleanup
        open_iters (int): Number of opening iterations (removes speckles)
        close_iters (int): Number of closing iterations (fills holes)
        enhance_dark (bool): Applies CLAHE to value channel for darker scenes
        clahe_clip (float): CLAHE clip limit for value-channel enhancement
    
    Returns:
        tuple: Image with bounding box and the mask used
    """
    # Default to red color in HSV
    if lower_hsv is None:
        lower_hsv = np.array([0, 70, 40])
    if upper_hsv is None:
        upper_hsv = np.array([12, 255, 255])
    
    # Read image and convert to HSV
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if enhance_dark:
        h_channel, s_channel, v_channel = cv2.split(hsv)
        clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=(8, 8))
        v_channel = clahe.apply(v_channel)
        hsv = cv2.merge((h_channel, s_channel, v_channel))
    
    # Create mask from HSV thresholding
    # Red wraps around the HSV hue axis, so include both low and high hue bands.
    mask_low_red = cv2.inRange(hsv, lower_hsv, upper_hsv)
    high_red_lower = np.array([170, lower_hsv[1], lower_hsv[2]])
    high_red_upper = np.array([180, 255, 255])
    mask_high_red = cv2.inRange(hsv, high_red_lower, high_red_upper)
    mask = cv2.bitwise_or(mask_low_red, mask_high_red)

    # Clean mask to reduce tiny noisy regions
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=open_iters)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=close_iters)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw bounding boxes around contours
    result = image.copy()
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if w < min_dimension and h < min_dimension:
            continue
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return result, mask

# Example usage:
# image_with_box, mask = create_color_bounding_box('image.jpg')
# cv2.imshow('Result', image_with_box)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
def main():
    
    dataset_path = r"C:\Users\kmpot\Downloads\dataset\red"
    
    for image_file in Path(dataset_path).glob("*"):
        if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            image_with_box, mask = create_color_bounding_box(str(image_file))
            cv2.imshow('Result', image_with_box)
            cv2.waitKey(0)
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

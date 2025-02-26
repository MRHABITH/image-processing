import cv2
import numpy as np

def apply_filter(image_path, filter_type):
    image = cv2.imread(image_path)

    if filter_type == "gray":
        filtered = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        filtered = cv2.transform(image, kernel)
    elif filter_type == "blur":
        filtered = cv2.GaussianBlur(image, (15, 15), 0)
    else:
        filtered = image

    output_path = image_path.replace(".jpg", f"_{filter_type}.jpg")
    cv2.imwrite(output_path, filtered)
    return output_path
import streamlit as st
import cv2
import os
import time
import qrcode
import uuid
import numpy as np
from PIL import Image

UPLOAD_FOLDER = "static/images/"
QR_FOLDER = "static/qr_codes/"
BASE_URL = "http://yourdomain.com/images/"  # Replace with your actual base URL

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

def capture_image():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        return None
    ret, frame = cam.read()
    cam.release()
    return frame if ret else None

def apply_filter(image, filter_type):
    filters = {
        "Grayscale": lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
        "Blur": lambda img: cv2.GaussianBlur(img, (15, 15), 0),
        "Edge Detection": lambda img: cv2.Canny(img, 100, 200),
    }
    return filters.get(filter_type, lambda img: img)(image)

def generate_qr(data):
    qr = qrcode.make(data)
    qr_filename = f"qr_{uuid.uuid4().hex}.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    qr.save(qr_path)
    return qr_path

st.title("Image Processing App")

# Capture image functionality
if st.button("Capture Image"):
    frame = capture_image()
    if frame is not None:
        filename = f"captured_{int(time.time())}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        cv2.imwrite(filepath, frame)
        st.image(frame, caption="Captured Image", use_column_width=True)
        st.session_state["image_path"] = filepath
    else:
        st.error("Failed to capture image.")

# Upload an image functionality
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    image.save(image_path)
    st.session_state["image_path"] = image_path
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Image filter functionality
if "image_path" in st.session_state:
    filter_type = st.selectbox("Select a Filter", ["None", "Grayscale", "Blur", "Edge Detection"])
    if st.button("Apply Filter"):
        image = cv2.imread(st.session_state["image_path"])
        if filter_type != "None":
            filtered_image = apply_filter(image, filter_type)
            output_filename = f"filtered_{int(time.time())}.jpg"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            cv2.imwrite(output_path, filtered_image)
            st.image(filtered_image, caption="Filtered Image", use_column_width=True)
            st.session_state["image_path"] = output_path

    # Generate QR code for image download link
    if st.button("Generate QR Code"):
        image_url = BASE_URL + os.path.basename(st.session_state["image_path"])
        qr_path = generate_qr(image_url)
        st.image(qr_path, caption="QR Code", use_column_width=True)
        st.write(f"Scan the QR code to download the image from: {image_url}")

    # Allow users to download the image directly
    if st.button("Download Image"):
        with open(st.session_state["image_path"], "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name=os.path.basename(st.session_state["image_path"]),
                mime="image/jpeg"
            )

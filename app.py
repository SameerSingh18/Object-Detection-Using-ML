from pathlib import Path
import streamlit as st
import PIL.Image
from ultralytics import YOLO

import settings

st.set_page_config(
    page_title="Object Detection",
    page_icon="📟",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Object Detection")

st.link_button(
    "About Us",
    "https://github.com/Divy-Gupta/Object-Detection/tree/main"
)

st.sidebar.header("Settings")

model_type = st.sidebar.radio(
    "Select Task",
    ["Normal_Detection", "PPE_Detection"]
)

confidence = st.sidebar.slider(
    "Select Model Confidence",
    25, 100, 40
) / 100

model_path = Path(
    settings.DETECTION_MODEL
    if model_type == "Normal_Detection"
    else settings.DETECTION_MODEL1
)

try:
    model = YOLO(model_path)
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

st.sidebar.header("Image Config")

source_img = st.sidebar.file_uploader(
    "Choose an image...",
    type=("jpg", "jpeg", "png", "bmp", "webp")
)

def display_image(image, caption):
    st.image(image, caption=caption, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    if source_img:
        uploaded_image = PIL.Image.open(source_img)
        display_image(uploaded_image, "Uploaded Image")
    else:
        default_image = PIL.Image.open(settings.DEFAULT_IMAGE)
        display_image(default_image, "Default Image")

with col2:
    if source_img and st.sidebar.button("Detect Objects"):
        results = model.predict(uploaded_image, conf=confidence)
        plotted = results[0].plot()[:, :, ::-1]
        display_image(plotted, "Detected Image")

        boxes = results[0].boxes
        if boxes is not None and len(boxes) > 0:
            with st.expander("Detection Results"):
                for box in boxes:
                    st.write(box.data)
        else:
            st.info("No objects detected")

    elif not source_img:
        default_detected = PIL.Image.open(
            settings.DEFAULT_DETECT_IMAGE
        )
        display_image(default_detected, "Detected Image")

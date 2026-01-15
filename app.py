from pathlib import Path
import streamlit as st
import PIL.Image

import settings
import helper

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
    ['Normal_Detection', 'PPE_Detection']
)

confidence = st.sidebar.slider(
    "Select Model Confidence",
    25, 100, 40
) / 100

model_path = Path(
    settings.DETECTION_MODEL
    if model_type == 'Normal_Detection'
    else settings.DETECTION_MODEL1
)

try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model from path: {model_path}")
    st.stop()

st.sidebar.header("Image / Video Config")
source_radio = st.sidebar.radio(
    "Select Source",
    settings.SOURCES_LIST
)
def display_image(image, caption):
    st.image(image, caption=caption, use_container_width=True)

if source_radio == settings.IMAGE:

    source_img = st.sidebar.file_uploader(
        "Choose an image...",
        type=("jpg", "jpeg", "png", "bmp", "webp")
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            try:
                uploaded_image = PIL.Image.open(source_img)
                display_image(uploaded_image, "Uploaded Image")
            except Exception as ex:
                st.error("Error opening image")
                st.stop()
        else:
            default_image = PIL.Image.open(settings.DEFAULT_IMAGE)
            display_image(default_image, "Default Image")

    with col2:
        if source_img and st.sidebar.button("Detect Objects"):
            res = model.predict(uploaded_image, conf=confidence)
            boxes = res[0].boxes

            res_plotted = res[0].plot()[:, :, ::-1]
            display_image(res_plotted, "Detected Image")

            if boxes is not None and len(boxes) > 0:
                with st.expander("Detection Results"):
                    for box in boxes:
                        st.write(box.data)
            else:
                st.info("No objects detected!")

        elif not source_img:
            default_detected_image = PIL.Image.open(
                settings.DEFAULT_DETECT_IMAGE
            )
            display_image(default_detected_image, "Detected Image")

elif source_radio == settings.WEBCAM:
    st.error(
        "Webcam is not supported on Streamlit Cloud. "
        "Please run locally."
    )

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type.")

import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
import streamlit
from pathlib import Path
import PIL.Image
import settings
import helper
import webbrowser
import streamlit as st 
# Setting page layout
st.set_page_config(
    page_title="Object Detection",
    page_icon="📟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Object Detection")
url = 'file:///C:/Users/HP/OneDrive/Desktop/object%20detection%20website/p1.html'

st.link_button("About Us", "https://github.com/Divy-Gupta/Object-Detection/tree/main")

# Sidebar
st.sidebar.header("Settings")

# Model Options
model_type = st.sidebar.radio("Select Task", ['Normal_Detection', 'PPE_Detection'])
confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Model
model_path = Path(settings.DETECTION_MODEL if model_type == 'Normal_Detection' else settings.DETECTION_MODEL1)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio("Select Source", settings.SOURCES_LIST)

source_img = None

# Function to display images
def display_image(image, caption):
    st.image(image, caption=caption, use_container_width=True)

# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp', 'svg'))

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            try:
                uploaded_image = PIL.Image.open(source_img)
                display_image(uploaded_image, "Uploaded Image")
            except Exception as ex:
                st.error("Error occurred while opening the image.")
                st.error(ex)
        else:
            default_image_path = str(settings.DEFAULT_IMAGE)
            display_image(default_image_path, "Default Image")

    with col2:
        if source_img:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                display_image(res_plotted, 'Detected Image')
                if boxes:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                else:
                    st.write("No objects detected!")
        else:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            display_image(default_detected_image_path, 'Detected Image')

elif source_radio == settings.WEBCAM:
     st.error("Sorry for inconvenience but streamlit cloud doesn't support webcam!!")
elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")

import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import rembg
import io
import zipfile
import os
import requests

# URL to the model
MODEL_URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
MODEL_PATH = "./models/u2net.onnx"

# Function to download the model if it doesn't exist
def download_model(url, model_path):
    if not os.path.exists(model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        response = requests.get(url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded model to {model_path}")

# Function to remove background
def remove_background(image, model_path):
    image_np = np.array(image)
    session = rembg.new_session(model_name='u2net', model_path=model_path)
    result = rembg.remove(image_np, session=session)
    result_image = Image.fromarray(result)
    white_bg_image = Image.new("RGBA", result_image.size, "WHITE")
    white_bg_image.paste(result_image, (0, 0), result_image)
    return white_bg_image.convert("RGB")

# Download the model if necessary
download_model(MODEL_URL, MODEL_PATH)

st.title("Bulk Background Remover and White Background Adder")

uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

if uploaded_files:
    with zipfile.ZipFile("processed_images.zip", "w") as zf:
        for uploaded_file in uploaded_files:
            # Read the image
            image = Image.open(uploaded_file)
            
            # Process the image
            result_image = remove_background(image)
            
            # Save the result to a buffer
            buffer = io.BytesIO()
            result_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Write the buffer to the zip file with the original file name
            zf.writestr(uploaded_file.name, buffer.read())
    
    with open("processed_images.zip", "rb") as f:
        st.download_button(
            label="Download All Images as ZIP",
            data=f,
            file_name="processed_images.zip",
            mime="application/zip"
        )

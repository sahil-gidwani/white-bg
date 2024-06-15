import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import rembg
import io
import zipfile

rembg.bg.get_model('u2net')

def remove_background(image):
    image_np = np.array(image)
    result = rembg.remove(image_np)
    result_image = Image.fromarray(result)
    white_bg_image = Image.new("RGBA", result_image.size, "WHITE")
    white_bg_image.paste(result_image, (0, 0), result_image)
    return white_bg_image.convert("RGB")

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

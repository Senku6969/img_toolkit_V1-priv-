import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps, ImageFont
import numpy as np
import cv2
import math
import io
import easyocr
from rembg import remove

def enhance_image(image, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0):
    img = ImageEnhance.Brightness(image).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img 

def apply_color_effect(image, effect):
    img_array = np.array(image)
    
    if effect == "Grayscale":
        return ImageOps.grayscale(image)
    elif effect == "Sepia":
        sepia_matrix = [
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ]
        sepia_array = cv2.transform(img_array, np.array(sepia_matrix))
        np.clip(sepia_array, 0, 255, out=sepia_array)
        return Image.fromarray(sepia_array.astype(np.uint8))
    elif effect == "Negative":
        return ImageOps.invert(image)
    elif effect == "Black & White":
        return image.convert('L').point(lambda x: 0 if x < 128 else 255, '1')
    return image

def apply_filter(image, filter_type):
    if filter_type == "Blur":
        return image.filter(ImageFilter.BLUR)
    elif filter_type == "Contour":
        return image.filter(ImageFilter.CONTOUR)
    elif filter_type == "Emboss":
        return image.filter(ImageFilter.EMBOSS)
    elif filter_type == "Edge Enhance":
        return image.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_type == "Smooth":
        return image.filter(ImageFilter.SMOOTH)
    elif filter_type == "Sharpen":
        return image.filter(ImageFilter.SHARPEN)
    return image

def detect_edges(image, threshold1=100, threshold2=200):
    """Detect edges using Canny algorithm"""
    img_array = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, threshold1, threshold2)
    return Image.fromarray(edges)

def remove_background(image):
    return remove(image)

def extract_text(image):
    reader = easyocr.Reader(["en"])
    result = reader.readtext(np.array(image))
    extracted_text = " ".join([text[1] for text in result])
    return extracted_text

def rotate_image(image, angle):
    return image.rotate(angle, expand=True)

def resize_image(image, width=None, height=None):
    if width and height:
        return image.resize((width, height))
    elif width:
        ratio = width / image.size[0]
        height = int(image.size[1] * ratio)
        return image.resize((width, height))
    elif height:
        ratio = height / image.size[1]
        width = int(image.size[0] * ratio)
        return image.resize((width, height))
    return image

def add_watermark(image, text, opacity=0.5):
    img = image.convert('RGBA')
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    x, y = img.size[0] - bbox[2] - 10, img.size[1] - bbox[3] - 10
    draw.text((x, y), text, font=font, fill=(255, 255, 255, int(255*opacity)))
    return Image.alpha_composite(img, txt).convert('RGB')

def add_frame(image, frame_width=10, frame_color=(0, 0, 0)):
    return ImageOps.expand(image, border=frame_width, fill=frame_color)

def add_vignette(image, intensity=0.5):
    img_array = np.array(image)
    rows, cols = img_array.shape[:2]
    
    # Generate vignette mask
    X_resultant, Y_resultant = np.meshgrid(np.arange(cols), np.arange(rows))
    centerX, centerY = cols/2, rows/2
    distance = np.sqrt((X_resultant - centerX)**2 + (Y_resultant - centerY)**2)
    
    # Normalize distances
    maxDistance = np.sqrt((centerX**2 + centerY**2))
    distance = distance/maxDistance
    
    # Create vignette mask
    vignetteMap = np.cos(distance * math.pi * intensity)
    vignetteMap = np.clip(vignetteMap, 0, 1)
    
    # Apply vignette
    for i in range(3):
        img_array[:,:,i] = img_array[:,:,i] * vignetteMap
        
    return Image.fromarray(img_array.astype(np.uint8))





# UI-----------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="AI Image Toolkit")
st.title("Senku's Image Toolkit")

#test

# sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        # Add download section in sidebar right after file upload
        st.markdown("---")  # Add a visual separator
        st.header("Download")
        download_format = st.selectbox("Download Format", ["PNG", "JPEG", "WebP"], 
                                     help="Choose the format for your downloaded image")
    
    st.header("Tools")
    feature = st.selectbox("Choose Tool:", [
        "Basic Enhancement", "Color Effects", "Edge Detection", "Background Removal",
        "Watermark", "Text OCR", "Rotate & Resize", 
        "Vignette Effect", "Frame", "Filters"
    ])
    
    if feature == "Basic Enhancement":
        brightness = st.slider("Brightness", 0.0, 2.0, 1.0, 0.1)
        contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1)
        saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1)
        sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0, 0.1)
    elif feature == "Text OCR":
        st.info("Extract text from images using OCR.")
    elif feature == "Color Effects":
        effect = st.selectbox("Select Effect", 
            ["Grayscale", "Sepia", "Negative", "Black & White"])
    elif feature == "Edge Detection":
        threshold1 = st.slider("Threshold 1", 0, 255, 100)
        threshold2 = st.slider("Threshold 2", 0, 255, 200)
    elif feature == "Filters":
        filter_type = st.selectbox("Select Filter", 
            ["Blur", "Contour", "Emboss", "Edge Enhance", "Smooth", "Sharpen"])
    elif feature == "Watermark":
        watermark_text = st.text_input("Watermark Text", "© 2025")
        opacity = st.slider("Opacity", 0.1, 1.0, 0.5)
    elif feature == "Frame":
        frame_width = st.slider("Frame Width", 1, 50, 10)
        frame_color = st.color_picker("Frame Color", "#000000")
    elif feature == "Rotate & Resize":
        angle = st.slider("Rotation Angle", -180, 180, 0)
        width = st.number_input("Width", min_value=1, max_value=4000, value=800)
        maintain_aspect = st.checkbox("Maintain Aspect Ratio", value=True) 
    elif feature == "Vignette Effect":
        vignette_intensity = st.slider("Intensity", 0.0, 1.0, 0.5)

# mains---
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    col1, col2 = st.columns(2)
    
    # col1 = orignal img
    with col1:
        st.image(image, caption="Original Image", use_column_width=True)
    
    # col2 = processed img
    with col2:
        with st.spinner("Processing..."):
            if feature == "Text OCR":
                text = extract_text(image)
                result = image
                st.image(image, caption="Processed Image", use_column_width=True)
                st.text_area("Extracted Text", text, height=200)
            else:
                if feature == "Basic Enhancement":
                    result = enhance_image(image, brightness, contrast, saturation, sharpness)
                elif feature == "Color Effects":
                    result = apply_color_effect(image, effect)
                elif feature == "Edge Detection":
                    result = detect_edges(image, threshold1, threshold2)
                elif feature == "Background Removal":
                    result = remove_background(image)
                elif feature == "Watermark":
                    result = add_watermark(image, watermark_text, opacity)
                elif feature == "Rotate & Resize":
                    rotated = rotate_image(image, angle)
                    if maintain_aspect:
                        result = resize_image(rotated, width=width)
                    else:
                        height = st.number_input("Height", min_value=1, max_value=4000, value=800)
                        result = resize_image(rotated, width, height)
                elif feature == "Vignette Effect":
                    result = add_vignette(image, vignette_intensity)
                elif feature == "Frame":
                    result = add_frame(image, frame_width, frame_color)
                elif feature == "Filters":
                    result = apply_filter(image, filter_type)
                
                st.image(result, caption=f"After {feature}", use_column_width=True)
    
# DOWNLOAD BUTTON 
    with st.sidebar:
        # Create a buffer to store the image
        buf = io.BytesIO()
    
        # Use the selected download format
        file_extension = download_format.lower()
        result.save(buf, format=download_format)
        byte_im = buf.getvalue()
        
        st.download_button(
            label=f"Download as {download_format}",
            data=byte_im,
            file_name=f"processed_image.{file_extension}",
            mime=f"image/{file_extension}",
            use_container_width=True  
        )



# PixelForge - AI Image Toolkit

PixelForge is an AI-powered image processing toolkit built with Python and Streamlit. It offers a variety of powerful tools for enhancing, editing, and transforming images using machine learning models and traditional image processing techniques.

## Features
- **Basic Enhancement**: Adjust brightness, contrast, saturation, and sharpness.
- **Color Effects**: Apply effects like Grayscale, Sepia, Negative, and Black & White.
- **Edge Detection**: Detect edges using customizable thresholds.
- **Background Removal**: Remove or replace image background with transparent or solid color.
- **Watermarking**: Add customizable watermarks with adjustable opacity, position, and font size.
- **Text OCR**: Extract text from images using Optical Character Recognition (OCR).
- **Rotate & Resize**: Rotate images and resize by width, height, or both while maintaining aspect ratio.
- **Vignette Effect**: Add a vignette effect with customizable intensity and color.
- **Filters**: Apply various filters like Blur, Emboss, Contour, Sharpen, and more.
- **Frame Addition**: Add customizable frames with solid, double, or shadow effects.
- **Pixel Enhancement**: Enhance image quality through denoising, upscaling, and sharpening.
- **Colorization**: Colorize grayscale images using machine learning.

## 💻 Tech Stack
- **Framework**: Streamlit
- **Computer Vision**: OpenCV, Pillow
- **AI Models**: Rembg (background removal), OpenCV Colorization
- **OCR**: EasyOCR
- **Image Processing**: NumPy, ImageEnhance

## ⚙️ Installation
1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/pixelforge.git
   cd pixelforge
   ```

2. Create and activate virtual environment:
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage
Run the Streamlit app:
```bash
streamlit run app.py
```
Access via browser at `http://localhost:8501`

## 📦 Requirements
- Python 3.8+
- See [requirements.txt](requirements.txt) for full list

**Note**: The colorization feature requires the following files in your project root:
- `colorization_deploy_v2.prototxt`
- `colorization_release_v2.caffemodel`
- `pts_in_hull.npy`

These can be downloaded from OpenCV's official repositories or using the provided installation commands.
🧠 TrueSight – Deepfake Detection System (Image, Video & Audio)

TrueSight is a deep learning–based Deepfake Detection System designed to identify manipulated media across images, videos, and audio. The system integrates CNN architectures, transfer learning techniques, and classical machine learning models to provide robust and reliable detection results.

🚀 Features

✅ Image Deepfake Detection

✅ Video Frame-by-Frame Analysis with Fake Frame Percentage

✅ Audio Deepfake Detection

✅ User Authentication System (Login & Registration)

✅ Detailed Analysis Report Generation

✅ Web-based Interface using Flask

🧩 Technologies Used

Backend: Flask (Python)

Deep Learning: TensorFlow / Keras (VGG16 + CNN)

Machine Learning: Random Forest (Scikit-learn)

Computer Vision: OpenCV, MTCNN

Audio Processing: Librosa

Database: SQLite

Deployment: Gunicorn

🏗 System Architecture

Media Input (Image / Video / Audio)

Preprocessing & Feature Extraction

Deep Learning Model Inference

Frame-level / Signal-level Analysis

Final Classification (REAL / FAKE)

Result Visualization via Web Interface

📊 Model Details

Transfer Learning using VGG16

Custom CNN layers for classification

Random Forest for auxiliary predictions

Frame-based video analysis with threshold-based decision logic

Performance evaluated using accuracy, precision, recall, and confusion matrix

📂 Project Structure
app.py
templates/
static/
models/
best_model.h5
random_forest_model.joblib
requirements.txt
Procfile
🎯 Use Cases

Fake media detection

Digital forensics research

Social media misinformation analysis

Academic deep learning experimentation

📌 Future Improvements

Multimodal fusion (Image + Audio + Metadata)

Real-time streaming detection

Model optimization for cloud deployment

API-based inference service

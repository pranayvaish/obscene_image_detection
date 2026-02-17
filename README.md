# obscene_image_detection
# NSFW / SFW Image Detection System using CNN

## 📌 Overview
This project is a Deep Learning–based NSFW (Not Safe For Work) Image Detection System that classifies images as Safe (SFW) or Not Safe (NSFW). It uses a Convolutional Neural Network (CNN) trained on labeled image data to automatically detect obscene or inappropriate content.

The project also includes a graphical user interface (GUI) built using Tkinter, allowing users to upload an image and instantly check whether it is safe or NSFW.

This system can be used in social media platforms, websites, and applications to prevent the upload of inappropriate content.

---

## 🎯 Features

- CNN-based deep learning model
- Classifies images as SFW or NSFW
- User-friendly GUI using Tkinter
- Real-time prediction
- Easy to use and integrate
- Trained on 10,000+ images

---

## 🧠 Model Information

The model uses a Convolutional Neural Network (CNN) consisting of:

- Convolution Layers
- MaxPooling Layers
- Flatten Layer
- Dense Layers
- Output Layer (Sigmoid activation)

Loss Function: Binary Crossentropy  
Optimizer: Adam  
Output: Binary classification (SFW or NSFW)

---

## 📂 Project Structure

|── final_gui.py
│ → GUI application for uploading and checking images
│
├── obscene_detect_10000.ipynb
│ → Jupyter Notebook containing model training and prediction code
│
├── README.md
│ → Project documentation


---

## 🖥️ GUI Application

The file `final_gui.py` contains the graphical user interface.

It allows users to:

- Upload an image
- Run the trained CNN model
- Display prediction result (SFW or NSFW)

This makes the system easy to use without programming knowledge.

---

## 📓 Model Training Notebook

The file `obscene_detect_10000.ipynb` contains:

- Dataset loading
- Image preprocessing
- CNN model creation
- Model training
- Model evaluation
- Model saving
- Prediction logic

---

## ⚙️ Technologies Used

- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Matplotlib
- Tkinter
- Jupyter Notebook

---



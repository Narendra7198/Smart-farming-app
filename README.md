# 🌾 Smart Crop Recommendation System

> An AI-powered web application that helps Indian farmers choose the right crop based on soil nutrients and live weather data.

![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)
![ML](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)

---

## 🚀 Live Demo

🌐 **Web App:** [Coming Soon — Deploying on Streamlit Cloud]

📱 **Android App:** Coming Soon on Google Play Store

🖥️ **Physical Device:** Smart Farming Machine — In Development

---

## 📌 About This Project

This project is built to solve a real problem faced by millions of Indian farmers — **which crop should I grow on my land?**

By entering simple soil test values (N, P, K, pH) and their city name, farmers get an instant AI-powered recommendation for the best crop suited to their exact field conditions — along with live weather data, farming tips, and a complete disease guide.

### What the system can do:
- ✅ Recommend the best crop based on soil + weather data
- ✅ Show live temperature, humidity, and rainfall for any city
- ✅ Complete disease guide for 7 major crops with symptoms, treatment, and prevention
- ✅ Detailed crop information for 22 crops — season, water need, soil type, and expert tips
- ✅ Fully mobile responsive — works on any phone or tablet

---

## 🗺️ Project Roadmap

This project is actively being developed. Here is the full plan:

| Phase | Feature | Status |
|-------|---------|--------|
| ✅ Phase 1 | AI Crop Recommendation Web App | **Complete** |
| ✅ Phase 1 | Disease Guide + Crop Information Pages | **Complete** |
| ✅ Phase 1 | Mobile Responsive Design | **Complete** |
| 🔄 Phase 2 | Deploy on Streamlit Cloud (Live Website) | **In Progress** |
| 🔄 Phase 3 | Android Mobile App | **Coming Soon** |
| 🔄 Phase 3 | Google Play Store Launch | **Coming Soon** |
| 🔄 Phase 4 | Physical Smart Farming Device (Raspberry Pi) | **Coming Soon** |

> **Note:** This README will be updated as each phase is completed.

---

## 🌿 Features

### 🌱 Crop Recommendation
- Enter soil N, P, K values and pH
- Enter your city — get live weather automatically
- AI model recommends the best crop instantly
- Shows season, water requirement, soil type, and farming tips

### 🦠 Disease Guide
Covers 7 major crops with detailed information:
- **Rice** — Blast, Bacterial Leaf Blight, Brown Spot
- **Wheat** — Yellow Rust, Leaf Rust, Loose Smut
- **Tomato** — Early Blight, Late Blight, Yellow Leaf Curl Virus
- **Potato** — Late Blight, Early Blight
- **Cotton** — Bollworm, Alternaria Blight
- **Maize** — Fall Armyworm, Northern Leaf Blight
- **Grapes** — Downy Mildew, Powdery Mildew

### 📊 Crop Information
Complete growing guide for 22 crops including Rice, Wheat, Maize, Tomato, Potato, Cotton, Mango, Banana, Apple, Grapes, Orange, Papaya, Coconut, Coffee, Jute, and more.

---

## 🤖 Technology Stack

| Component | Technology |
|-----------|-----------|
| ML Model | Random Forest Classifier |
| Model Accuracy | 99.3% |
| Dataset | Crop Recommendation Dataset (2,200 samples, 22 crops) |
| Weather API | OpenWeatherMap Live API |
| Web Framework | Streamlit |
| Language | Python 3 |
| Deployment | Streamlit Cloud |

---

## 📊 Dataset

- **File:** `Data/Crop_recommendation.csv`
- **Samples:** 2,200 rows
- **Features:** Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, Rainfall
- **Target:** 22 crop classes
- **Train / Test Split:** 80% / 20%

---

## 📁 Project Structure

```
smart-farming-app/
│
├── app.py                        ← Main Streamlit web application
├── requirements.txt              ← Python dependencies
│
├── Model/
│   └── crop_model.pkl            ← Trained ML model
│
└── Data/
    └── Crop_recommendation.csv   ← Training dataset
```

---

## ⚙️ How to Run Locally

```bash
# Step 1 — Clone the repository
git clone https://github.com/Narendra7198/smart-farming-app.git
cd smart-farming-app

# Step 2 — Install dependencies
pip install -r requirements.txt

# Step 3 — Run the app
streamlit run app.py

# Step 4 — Open in browser
http://localhost:8501
```

---

## 📱 Android App (Coming Soon)

An Android application is currently in development. It will be available on the **Google Play Store** soon.

The app will allow farmers to:
- Use the crop recommendation system directly from their phone
- Access the disease guide offline
- Get instant results without opening a browser

---

## 🖥️ Smart Farming Physical Device (Coming Soon)

A physical portable device is being developed for use directly in the field. It will include:
- A camera to capture leaf images for disease detection
- Soil sensor to read NPK values automatically
- A small touchscreen to show results
- Battery-powered — no electricity needed in the field

This device will allow farmers to get crop and disease information without a smartphone or internet connection.

---

## 👨‍💻 Developer

**Narendra Singh Panwar**

---

## 📄 License

This project is open source and free to use for agricultural and educational purposes.

---

*This project is built to help Indian farmers make better decisions using technology.*

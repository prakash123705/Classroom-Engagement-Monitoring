# 🎓 Real-Time Classroom Student Engagement Monitoring System

An AI-powered classroom monitoring system that detects students, tracks them in real time, extracts facial features, predicts engagement levels using Machine Learning, and visualizes classroom analytics through an interactive Streamlit dashboard.

---

## 📖 Overview

This project combines Computer Vision, Deep Learning, and Machine Learning techniques to automatically monitor student engagement during classroom sessions.

The system performs the following tasks:

- Detects students using YOLOv5
- Tracks each student using DeepSORT
- Detects faces using OpenCV Haar Cascade
- Extracts facial features using DenseNet121
- Predicts engagement using a Random Forest classifier
- Calculates overall classroom engagement percentage
- Displays real-time analytics in a Streamlit dashboard
- Stores engagement reports in CSV format

---

## ✨ Features

- 🎯 Real-time student detection
- 👥 Multi-object tracking
- 😀 Face detection
- 🧠 DenseNet121 feature extraction
- 🤖 Random Forest engagement prediction
- 📊 Live engagement statistics
- 📈 Interactive dashboard
- 💾 Automatic CSV report generation
- 🆔 Student ID tracking
- 📥 Downloadable reports

---

## 🛠 Technologies Used

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Computer Vision | OpenCV, YOLOv5 |
| Object Tracking | DeepSORT |
| Deep Learning | TensorFlow, Keras, DenseNet121 |
| Machine Learning | Scikit-learn, Random Forest |
| Dashboard | Streamlit, Plotly |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib |

---

## 📂 Project Structure

```text
Classroom-Engagement-Monitoring/
│
├── app.py
├── dashboard.py
├── train_random_forest.py
├── create_centroids.py
├── face_id_detection.py
│
├── DATASET_Engagement_Binary.csv
├── rf_model_final.pkl
├── engaged_centroid.pkl
├── disengaged_centroid.pkl
│
├── sessions/
│
├── requirements.txt
├── README.md
└── assets/
```

---

## ⚙️ System Workflow

```
Live Camera
      │
      ▼
YOLOv5 Person Detection
      │
      ▼
DeepSORT Tracking
      │
      ▼
Face Detection
      │
      ▼
DenseNet121 Feature Extraction
      │
      ▼
Random Forest Classification
      │
      ▼
Engagement Prediction
      │
      ▼
CSV Report Generation
      │
      ▼
Streamlit Dashboard
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/your-username/Classroom-Engagement-Monitoring.git
```

Go to the project folder

```bash
cd Classroom-Engagement-Monitoring
```

Install the required packages

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Start the dashboard

```bash
streamlit run dashboard.py
```

Click **Start Monitoring** to begin real-time classroom analysis.

---

## 📊 Dashboard Features

- Total Students
- Engaged Students
- Disengaged Students
- Classroom Engagement Percentage
- Live Status
- Gauge Chart
- Pie Chart
- Student Records
- CSV Download

---

## 📈 Output

The system provides:

- Student IDs
- Engagement Status
- Engagement Probability
- Classroom Engagement Percentage
- CSV Reports
- Interactive Dashboard

---

## 🎯 Applications

- Smart Classrooms
- Educational Analytics
- Online Learning Monitoring
- Student Engagement Analysis
- AI-based Education Systems

---

## 🔮 Future Enhancements

- Emotion Recognition
- Eye Gaze Tracking
- Head Pose Estimation
- Multi-Camera Monitoring
- Cloud Deployment
- Database Integration
- Mobile Application
- Attendance Analytics

---

## 👨‍💻 Author

**Prakash Mogga**

B.Tech – Computer Science and Engineering

Areas of Interest:

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Computer Vision

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

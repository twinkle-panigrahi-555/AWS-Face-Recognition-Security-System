# AWS Face Recognition Smart Security System 🔐

This project is a real-time face recognition security system using
AWS Rekognition, OpenCV, and Python.

## 🔹 Features
- Real-time webcam face detection
- AWS Rekognition face matching
- Authorized / Unauthorized access control
- Displays employee details after authentication

## 🔹 Technologies Used
- Python
- OpenCV
- AWS Rekognition
- Amazon S3

## 🔹 How It Works
1. Employee images are stored in Amazon S3
2. Faces are indexed into AWS Rekognition
3. Webcam captures live face
4. Face is compared with stored faces
5. Access is granted or denied

## 🔹 How to Run
```bash
pip install -r requirements.txt
python webcam_access.py

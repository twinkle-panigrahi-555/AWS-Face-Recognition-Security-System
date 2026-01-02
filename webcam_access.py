import cv2
import boto3
import numpy as np
from employee_info import employees  # ⭐ Employee database

# AWS Rekognition Client
rekognition = boto3.client('rekognition', region_name='us-east-1')
collection_id = "authorized_people"

# Load OpenCV Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     "haarcascade_frontalface_default.xml")

def search_face_in_aws(face_image):
    _, buffer = cv2.imencode('.jpg', face_image)
    img_bytes = buffer.tobytes()

    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': img_bytes},
        MaxFaces=1,
        FaceMatchThreshold=85
    )

    if len(response['FaceMatches']) > 0:
        match = response['FaceMatches'][0]
        name = match['Face']['ExternalImageId']
        similarity = match['Similarity']
        print(f"\n✔ MATCH FOUND ➜ {name} ({int(similarity)}%)")
        return name, similarity
    else:
        print("\n❌ Not a registered employee!")
        return None, None


# Start Webcam
cap = cv2.VideoCapture(0)
print("\n🎥 Smart Security System Started — Press 'Q' to Quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_img = frame[y:y+h, x:x+w]

        name, similarity = search_face_in_aws(face_img)

        if name:
            color = (0, 255, 0)
            cv2.putText(frame, f"ACCESS GRANTED: {name}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, color, 2)

            # ⭐ Show Employee Details
            if name in employees:
                dept = employees[name]["Department"]
                phone = employees[name]["Phone"]

                cv2.putText(frame, f"Dept: {dept}",
                            (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, color, 2)

                cv2.putText(frame, f"Phone: {phone}",
                            (20, 120), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, color, 2)
        else:
            color = (0, 0, 255)
            cv2.putText(frame, "ACCESS DENIED",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, color, 2)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    else:
        cv2.putText(frame, "⚠ No Face Detected!",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 2)

    cv2.imshow("Twinkle's Smart Security System 🔐", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\nCamera Closed!\n")

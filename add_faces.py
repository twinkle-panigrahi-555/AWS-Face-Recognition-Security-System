import boto3
import os

rekognition = boto3.client("rekognition")

collection_id = "authorized_people"
bucket_name = "twinkle-face-storage"

def index_faces():
    files = [
        "Bhumi.jpg",
        "Deepak.jpg",
        "Rohit.jpg",
        "Sneha.jpg",
        "kabir.jpg",
        "laxmi.jpg",
        "rohan.jpg",
        "roshni.jpg",
        "sania.jpg",
        "sonali.jpg",
        "subham.jpg",
        "subhasree.jpg",
        "suman.jpg"
    ]

    for file in files:
        print(f"Adding {file}...")
        response = rekognition.index_faces(
            CollectionId=collection_id,
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": file
                }
            },
            ExternalImageId=file.split(".")[0],  # Name without .jpg
            MaxFaces=1,
            DetectionAttributes=["DEFAULT"]
        )
        print("Done ✔")

if __name__ == "__main__":
    index_faces()
    print("\nAll 13 faces added to Rekognition successfully! 🎉")

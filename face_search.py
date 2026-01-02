import boto3

rekognition = boto3.client("rekognition")
collection_id = "authorized_people"
bucket_name = "twinkle-face-storage"

def search_face(image_name):
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": image_name
            }
        },
        FaceMatchThreshold=85,
        MaxFaces=1
    )

    if len(response['FaceMatches']) > 0:
        match = response['FaceMatches'][0]
        name = match['Face']['ExternalImageId']
        similarity = round(match['Similarity'], 2)

        print("\n------ MATCH FOUND ------")
        print(f"Employee Name : {name}")
        print(f"Similarity    : {similarity}%")
        print("-------------------------")
        print("✔ ACCESS AUTHORIZED\n")
        return True
    else:
        print("\n❌ Not a registered employee!")
        return False


if __name__ == "__main__":
    img = input("Enter employee image name : ")
    search_face(img)

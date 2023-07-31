import os
import pandas as pd
import face_recognition
import pickle


def check_image_exists(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError("No such img.")
    return True


def load_image_and_generate_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        raise ValueError("No faces found in the image.")
    return face_encodings


def get_known_face_encodings(folder_path, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            known_face_encodings = pickle.load(f)
    else:
        known_face_encodings = {}
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image = face_recognition.load_image_file(os.path.join(folder_path, filename))
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    known_face_encodings[filename] = face_encodings[0]
        with open(file_path, 'wb') as f:
            pickle.dump(known_face_encodings, f)
    return known_face_encodings


def compare_faces(unknown_face_encodings, known_face_encodings):
    matched_faces = []
    for unknown_face_encoding in unknown_face_encodings:
        for filename, known_face_encoding in known_face_encodings.items():
            results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=0.5)
            if results[0]:
                matched_faces.append(filename.split('.')[0])
    return matched_faces


def get_person_info(matched_faces):
    df = pd.read_excel('info.xlsx')
    matched_persons = []
    for person_id in matched_faces:
        person_info = df[df['id'].astype(str) == person_id]
        if not person_info.empty:
            matched_persons.append(person_info.iloc[0].to_dict())
    return matched_persons


def find_person_info(image_path):
    check_image_exists(image_path)
    unknown_face_encodings = load_image_and_generate_encodings(image_path)
    known_face_encodings = get_known_face_encodings("db", "face_encodings.pkl")
    matched_faces = compare_faces(unknown_face_encodings, known_face_encodings)
    matched_persons = get_person_info(matched_faces)
    return matched_persons

# print(find_person_info("upload/twoman.png"))

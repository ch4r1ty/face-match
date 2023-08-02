import datetime
import os
import pandas as pd
import face_recognition
import pickle
import time
from parameter import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import builtins

df = pd.read_excel('info.xlsx')

start_time = time.time()


def load_image_and_generate_encodings(fp):
    image = face_recognition.load_image_file(fp)
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

    def compare_face(unknown_face_encoding):
        for filename, known_face_encoding in known_face_encodings.items():
            results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance)
            if results[0]:
                return filename.split('.')[0]
        return None

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(compare_face, face_encoding): face_encoding for face_encoding in
                   unknown_face_encodings}

        for future in as_completed(futures):
            face = futures[future]
            try:
                result = future.result()
                if result is not None:
                    matched_faces.append(result)
            except Exception as exc:
                print('%r generated an exception: %s' % (face, exc))

    return matched_faces


def get_person_info(matched_faces):
    matched_persons = []
    for person_id in matched_faces:
        person_info = df[df['id'].astype(str) == person_id]
        if not person_info.empty:
            matched_persons.append(person_info.iloc[0].to_dict())
    return matched_persons


def find_person_info(file):
    unknown_face_encodings = load_image_and_generate_encodings(file)
    known_face_encodings = get_known_face_encodings("db", "face_encodings.pkl")
    matched_faces = compare_faces(unknown_face_encodings, known_face_encodings)
    matched_persons = get_person_info(matched_faces)
    return matched_persons


end_time = time.time()
running_time = end_time - start_time
print(running_time)

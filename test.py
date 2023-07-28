import os
import pandas as pd
import face_recognition


def check_image_exists(image_path):
    # 检查图片文件是否存在，如果不存在则抛出FileNotFoundError异常
    if not os.path.exists(image_path):
        raise FileNotFoundError("No such img.")
    return True


def load_image_and_generate_encodings(image_path):
    # 加载图片并生成面部编码，如果图片中没有人脸则抛出ValueError异常
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        raise ValueError("No faces found in the image.")
    return face_encodings


def get_known_face_encodings(folder_path):
    # 遍历指定文件夹，加载每一张图片并生成面部编码
    known_face_encodings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(folder_path, filename))
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                known_face_encodings[filename] = face_encodings[0]
    return known_face_encodings


def compare_faces(unknown_face_encodings, known_face_encodings):
    # 比较未知面部编码和已知面部编码，如果匹配则将匹配的人脸添加到列表中
    matched_faces = []
    for unknown_face_encoding in unknown_face_encodings:
        for filename, known_face_encoding in known_face_encodings.items():
            results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=0.5)
            if results[0]:
                matched_faces.append(filename.split('.')[0])
    return matched_faces


def get_person_info(matched_faces):
    # 从Excel文件中获取匹配的人脸的信息
    df = pd.read_excel('info.xlsx')
    matched_persons = []
    for person_id in matched_faces:
        person_info = df[df['id'].astype(str) == person_id]
        if not person_info.empty:
            matched_persons.append(person_info.iloc[0].to_dict())
    return matched_persons


def find_person_info(image_path):
    # 主函数，调用上述函数进行人脸识别
    check_image_exists(image_path)
    unknown_face_encodings = load_image_and_generate_encodings(image_path)
    known_face_encodings = get_known_face_encodings("db")
    matched_faces = compare_faces(unknown_face_encodings, known_face_encodings)
    matched_persons = get_person_info(matched_faces)
    return matched_persons

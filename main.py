import datetime
import os
import pandas as pd
import face_recognition
import pickle
import time
from parameter import *
from concurrent.futures import ThreadPoolExecutor, as_completed

start_time = time.time()


# 检查给定路径的图像文件是否存在。
# 如果文件不存在，抛出 FileNotFoundError。
def check_image_exists(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError("No such img.")
    return True


# 加载给定路径的图像文件，并生成面部编码
# 如果图像中没有面部，抛出 ValueError
def load_image_and_generate_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        raise ValueError("No faces found in the image.")
    return face_encodings


# 从给定的文件夹路径加载已知的面部编码，或者从给定的文件路径加载已保存的面部编码。
# 如果文件不存在，将从文件夹中的图像生成面部编码，并保存到文件中。
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


# 从Excel文件中获取匹配的面部的信息
def compare_faces(unknown_face_encodings, known_face_encodings):
    # 创建一个空列表来存储匹配的面部
    matched_faces = []

    # 定义一个内部函数，它接受一个未知的面部编码作为参数
    def compare_face(unknown_face_encoding):
        # 对于每个已知的面部编码
        # known_face_encodings.items()方法返回一个包含字典所有项的列表，每个项是一个元组，元组的第一个元素是键，第二个元素是值。
        for filename, known_face_encoding in known_face_encodings.items():
            # 使用face_recognition.compare_faces函数来比较未知的面部编码和已知的面部编码
            results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance)
            # 如果找到匹配的面部，返回匹配的面部的文件名（不包括扩展名）
            if results[0]:
                return filename.split('.')[0]
        # 如果没有找到匹配的面部，返回None
        return None

    # 创建一个ThreadPoolExecutor实例，这是一个线程池。max_workers=4参数表示线程池中最多可以有4个线程同时运行
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 使用executor.submit方法为每个未知的面部编码提交一个任务到线程池
        # 每个任务就是调用compare_face函数并传入一个未知的面部编码
        # executor.submit方法返回一个Future对象，这个对象代表一个尚未完成的计算
        # Future对象代表一个尚未完成的计算。当提交一个任务到ThreadPoolExecutor（或者其他类型的Executor），它会立即返回一个Future对象
        futures = {executor.submit(compare_face, face_encoding): face_encoding for face_encoding in unknown_face_encodings}

        # 使用as_completed函数来迭代已完成的Future对象
        for future in as_completed(futures):
            # 对于每个已完成的Future对象，获取它的结果（即compare_face函数的返回值）
            face = futures[future]
            try:
                result = future.result()
                # 如果结果不是None，就将结果添加到matched_faces列表中
                if result is not None:
                    matched_faces.append(result)
            # 如果在获取结果时发生异常，打印一个错误消息
            except Exception as exc:
                print('%r generated an exception: %s' % (face, exc))

    # 返回matched_faces列表，这个列表包含了所有匹配的面部的文件名
    return matched_faces


# 从Excel文件中获取匹配的面部的信息
def get_person_info(matched_faces):
    df = pd.read_excel('info.xlsx')
    matched_persons = []
    for person_id in matched_faces:
        person_info = df[df['id'].astype(str) == person_id]
        if not person_info.empty:
            matched_persons.append(person_info.iloc[0].to_dict())
    return matched_persons


# 主函数，调用上述函数进行人脸识别。
def find_person_info(image_path):
    check_image_exists(image_path)
    unknown_face_encodings = load_image_and_generate_encodings(image_path)
    known_face_encodings = get_known_face_encodings("db", "face_encodings.pkl")
    matched_faces = compare_faces(unknown_face_encodings, known_face_encodings)
    matched_persons = get_person_info(matched_faces)
    return matched_persons


# 打印时间，用来调试效率
end_time = time.time()
running_time = end_time-start_time
print(running_time)

print(find_person_info("upload/eason.png"))

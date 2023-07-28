import os
import pandas as pd
import face_recognition


def find_person_info(image_path):
    # 检查图片文件是否存在
    if not os.path.exists(image_path):
        return [], "No such img."

    # 文件夹路径
    folder_path = "db"

    # 加载你想要识别的图片
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)

    if not unknown_face_encodings:
        return [], "No faces found in the unknown_image."

    matched_persons = []  # 用于存储所有匹配的人的信息

    # 遍历图片中的每个面部编码
    for unknown_face_encoding in unknown_face_encodings:
        print(unknown_face_encoding)

        # 遍历文件夹中的每一张图片
        for filename in os.listdir(folder_path):
            # 只处理图片文件
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # 加载已知的图片
                known_image = face_recognition.load_image_file(os.path.join(folder_path, filename))
                known_face_encodings = face_recognition.face_encodings(known_image)

                if not known_face_encodings:
                    continue

                # 获取已知图片中的面部编码
                known_face_encoding = known_face_encodings[0]

                # 比较两个面部编码，看是否匹配，调整tolerance参数，取0.45差不多，还要调
                results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=0.5)

                # 打印结果
                if results[0]:
                    # 提取出不含后缀的文件名，假设文件名（不包括扩展名）是人的名字
                    person_id = filename.split('.')[0]

                    df = pd.read_excel('info.xlsx')

                    person_info = df[df['id'].astype(str) == person_id]

                    # 如果找到了这个人的信息
                    if not person_info.empty:
                        # 添加这个人的信息到列表中
                        matched_persons.append(person_info.iloc[0].to_dict())

    if matched_persons:
        return matched_persons, None
    else:
        return [], "No match found."

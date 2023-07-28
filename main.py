import face_recognition
import os
import pandas as pd

# 文件夹路径
folder_path = "db"

# 加载你想要识别的图片
unknown_image = face_recognition.load_image_file("caijianya.png")
unknown_face_encodings = face_recognition.face_encodings(unknown_image)

if not unknown_face_encodings:
    print("No faces found in the unknown_image.")
    exit()

# 获取未知图片中的面部编码
unknown_face_encoding = unknown_face_encodings[0]

# 遍历文件夹中的每一张图片
for filename in os.listdir(folder_path):
    # 只处理图片文件
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # 加载已知的图片
        known_image = face_recognition.load_image_file(os.path.join(folder_path, filename))
        known_face_encodings = face_recognition.face_encodings(known_image)

        if not known_face_encodings:
            print(f"No faces found in the image {filename}.")
            continue

        # 获取已知图片中的面部编码
        known_face_encoding = known_face_encodings[0]

        # 比较两个面部编码，看是否匹配，调整tolerance参数
        results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=0.45)

        # 打印结果
        if results[0]:
            # 提取出不含后缀的文件名，假设文件名（不包括扩展名）是人的名字
            person_id = filename.split('.')[0]
            print(f"The unknown_image has a face that matches {person_id}!")

            df = pd.read_excel('info.xlsx')

            person_info = df[df['id'].astype(str) == person_id]

            # 如果找到了这个人的信息
            if not person_info.empty:
                # 打印这个人的信息
                print(person_info.iloc[0])




# print(unknown_face_encoding)
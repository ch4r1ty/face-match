from deepface import DeepFace
import pandas as pd
import datetime
# 这个文件用之前要改成main.py

# Representations stored in db/representations_vgg_face.pkl file.Please delete this file when you add new identities in your database.
# 每次动db文件夹，也就是数据库，都要把里面的pkl文件删掉

# 读取 Excel 文件
df = pd.read_excel('info.xlsx')

a=datetime.datetime.now()

# 比对图片和数据库
# 这个是模版
# found = DeepFace.find(img_path = "img.png", db_path = "db")
found = DeepFace.find(img_path="img.png", db_path="db", model_name='DeepFace')

b=datetime.datetime.now()

# 如果找到了匹配的图片
if found:
    # 取第一张匹配的图片
    match = found[0]

    # 提取出不含后缀的文件名，假设找到的图片的文件名（不包括扩展名）是人的 ID
    person_id = str(match['identity']).split('/')[-1].split('.')[0]

    # 在 Excel 文件中查找这个人的信息
    person_info = df[df['id'].astype(str) == person_id]

    # 如果找到了这个人的信息
    if not person_info.empty:
        # 打印这个人的信息
        print(person_info.iloc[0])

# print("used time:", b-a)
# # 这里用来测试打印
# print(df)
# print('found:', found)
# print('person_id:', person_id)
# print('person_info:', person_info)
#



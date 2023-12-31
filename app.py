from flask import Flask, request, jsonify
from main import find_person_info  # 确保你的function.py文件在同一目录下，或者在Python的搜索路径中

app = Flask(__name__)


@app.route('/find_person_info', methods=['POST'])
def find_person_info_api():
    image_path = request.json['image_path']
    try:
        persons_info = find_person_info(image_path)
        return jsonify(persons_info), 200
    except FileNotFoundError:
        return jsonify({"message": "The image does not exist."}), 200
    except ValueError as e:
        if str(e) == "No faces found in the image.":
            return jsonify({"message": "No faces found in the uploaded image."}), 200
        elif "No faces found in the image" in str(e):
            return jsonify({"message": "No faces found in one of the known images."}), 200
    except Exception:
        return jsonify({"message": "No match found."}), 200


if __name__ == '__main__':
    app.run(debug=True)

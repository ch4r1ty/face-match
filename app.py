from flask import Flask, request, jsonify, render_template
# from werkzeug.utils import secure_filename
from main import find_person_info  # 确保你的main.py文件在同一目录下，或者在Python的搜索路径中
# from io import BytesIO

app = Flask(__name__)


@app.route('/find_person_info', methods=['POST', 'GET'])
def find_person_info_api():
    if 'image' not in request.files:
        return jsonify({"message": "No image file in the request."}), 400
    file = request.files['image']

    try:
        persons_info = find_person_info(file.stream)
        return jsonify(persons_info), 200
    except FileNotFoundError:
        return jsonify({"message": "The image does not exist."}), 200
    except ValueError as e:
        if str(e) == "No faces found in the image.":
            return jsonify({"message": "No faces found in the uploaded image."}), 200
        elif "No faces found in the image" in str(e):
            return jsonify({"message": "No faces found in one of the known images."}), 200
        return jsonify(persons_info), 200
    except Exception as e:
        return jsonify({"message": e}), 200


@app.route('/', methods=['GET'])
def upload_form():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)

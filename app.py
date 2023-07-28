from flask import Flask, request, jsonify
# from function import find_person_info
from test import check_image_exists, load_image_and_generate_encodings, get_known_face_encodings, compare_faces, get_person_info, find_person_info
import pandas as pd

app = Flask(__name__)


@app.route('/find_person_info', methods=['POST'])
def find_person_info_api():
    image_path = request.json['image_path']
    persons_info, error_message = find_person_info(image_path)
    if persons_info:
        return jsonify(persons_info), 200
    elif error_message == "No such img.":
        return jsonify({"message": "The image does not exist."}), 200
    elif error_message == "No faces found in the unknown_image.":
        return jsonify({"message": "No faces found in the uploaded image."}), 200
    elif "No faces found in the image" in error_message:
        return jsonify({"message": "No faces found in one of the known images."}), 200
    else:
        return jsonify({"message": "No match found."}), 200


if __name__ == '__main__':
    app.run(debug=True)

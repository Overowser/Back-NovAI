from flask import Flask, request, jsonify
from backshot import get_text
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)
@app.route("/kherya/", methods=["POST"])
def get_user():
    print(request.get_json())
    keyword = request.get_json()["keyword"]
    chapter = request.get_json()["chapter"]
    number = request.get_json()["number"]
    user_data = get_text(keyword, chapter, number)
    return jsonify(user_data), 200

if __name__ == "__main__":
    app.run(debug=True)
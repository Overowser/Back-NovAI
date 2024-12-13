from flask import Flask, request, jsonify
from backshot import get_text
# from backshot_async import get_text
from flask_cors import CORS, cross_origin
import asyncio


app = Flask(__name__)
CORS(app)
@app.route("/api/", methods=["POST"])
def get_user():
    req = request.get_json()
    user_data = asyncio.run(get_text(req["keyword"], req["chapter"], req["number"]))
    return jsonify(user_data), 200

if __name__ == "__main__":
    app.run(debug=True)
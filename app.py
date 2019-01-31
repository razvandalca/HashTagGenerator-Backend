import os

from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from image_processing import ImageProcessingThread

UPLOAD_FOLDER = '/IMAGES/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('localhost', 27017)
db = client.app_database
processing = ImageProcessingThread(db.images)
processing.start()

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/user/create", methods=['POST'])
def create_user():
    # Add better verification of data and to something with the key names
    form_data = request.form
    user_collection = db.user_collection
    username = form_data.get("username")
    email = form_data.get("email")
    password = form_data.get("password")
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")

    if all(v is not None for v in [username, password, email, password, first_name, last_name]):
        user_id = user_collection.insert({
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        })
        return "That fucinkg worked the useri id is  {}".format(user_id)
    else:
        return abort(400, "Bad request data missing")


@app.route("/user", methods=['GET'])
def get_user():
    # Make the query take into account all args sent with the keys
    args = request.args
    users = db.user_collection.find({"username": args.get("username")})
    return dumps(users)


@app.route("/upload", methods=['POST'])
def upload_image():
    file = request.files["image"]

    if file is None:
        abort(400, "Bad request , No file found")
    if request.form.get("user_id") is None:
        abort(400, "Bad request , User id not found")
    filename = secure_filename(file.filename)
    file.save(filename)

    image_id = db.images.insert({"user_id": request.form.get("user_id"),
                                 "processed": False,
                                 "path": app.root_path + "/" + filename}
                                )

    return "File {name} saved with the id {}".format(image_id, name=filename)

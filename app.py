import os
from io import BytesIO

from PIL import Image

from flask import Flask, request, jsonify, abort
from flask_mongoengine import wtf
from models import *
from flask_wtf import CSRFProtect

UPLOAD_FOLDER = '/IMAGES/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True
app.config['MONGODB_SETTINGS'] = {'DB': 'TESTDB'}
app.config.update(dict(
    SECRET_KEY="secret1",
    WTF_CSRF_SECRET_KEY="secret2",
    WTF_CSRF_ENABLED=False

))
db.init_app(app)
csrf = CSRFProtect()

if __name__ == '__main__':
    app.run(port=27017)
    csrf.init_app(app)


@app.route("/user/create", methods=['POST'])
def create_user():
    form = wtf.model_form(User)(request.form)
    if not form.validate():
        return jsonify({"errors": form.errors}), 400
    else:
        user = form.save()
        return jsonify(user)


@app.route("/user", methods=['GET'])
def get_user():
    # Make the query take into account all args sent with the keys
    user_id = request.args.get("user_id")
    if user_id is None:
        users = User.objects()
    else:
        users = User.objects(id=user_id).first()
    return jsonify(users)


@app.route("/image/upload", methods=['POST'])
def upload_image():
    image_entry = ImageUpload()
    # user = User.objects.get(id=request.form["user_id"])
    # image_entry.user = user
    file = request.files["image"]
    image_entry.image.new_file()
    image_entry.image.write(file.stream)
    image_entry.image.close()

    try:
        image_entry.validate()
    except ValidationError as e:
        return jsonify({"errors": str(e)}), 400

    image_entry = image_entry.save()
    return jsonify(image_entry)


@app.route("/image", methods=['GET'])
def get_image():
    image_id = request.args.get("image_id")
    image_entry = ImageUpload.objects(id=image_id).first()
    photo = image_entry.image.read()
    content_type = image_entry.image.content_type
    im = Image.open(BytesIO(photo))
    im.show()
    return jsonify(image_entry.tags)

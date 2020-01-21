import os
import logging

from werkzeug import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/auth")
def nginx_auth():
    original_uri = request.headers.get('X-Original-Uri')
    app.logger.info(
        'Flask route: nginx_auth, X-Original-Uri={original_uri}'.format(
            original_uri=original_uri))
    if original_uri != '/static/secret.txt':
        app.logger.info("Authorized")
        return "Authentication succesfull."
    else:
        app.logger.info("Unauthorized")
        return 'Unauthorized.', 401


@app.route("/")
def hello_world():
    app.logger.info('Flask route: hello_world')
    return jsonify(hello="world")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    app.logger.info('Flask route: staticfiles')
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    app.logger.info('Flask route: mediafiles')
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    app.logger.info('Flask route: upload_file')
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return f"""
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """

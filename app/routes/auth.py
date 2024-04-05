from flask import request, jsonify
from server import app, bcrypt
from app.schema.User import User
from app.schema.Property import MasterPropertyType, Property
from app.extensions.db import db
from app.extensions.responses import response_base


@app.route("/_health", methods=["GET"])
def health():
    # raise Exception("Health check failed")
    db.create_all()
    return "hi"


@app.route("/register007", methods=["POST"])
def register007():
    pwd_hash = bcrypt.generate_password_hash(request.json["password"])
    user = User(username=request.json["username"], password=pwd_hash)
    db.session.add(user)
    db.session.commit()
    return response_base(message="Success", status=200)


@app.route("/login", methods=["POST"])
def all():
    # db.create_all()
    data = request.json
    students = User.query.filter_by(username=request.json["username"]).first()
    print(students)
    if (students is not None) and bcrypt.check_password_hash(
        students.password, request.json["password"]
    ):
        return response_base(message="Success", status=200)
    else:
        return response_base(message="Failed", status=404)

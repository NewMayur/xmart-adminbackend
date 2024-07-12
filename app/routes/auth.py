from flask import request, jsonify
from server import app, bcrypt
from app.schema.User import User
from app.schema.Property import MasterPropertyType, Property
from app.extensions.db import db
from app.extensions.responses import response_base
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


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
    return response_base(message="Success", status=200,data=[])


# @app.route("/login", methods=["POST"])
# def all():
#     # db.create_all()
#     student = User.query.filter_by(username=request.json["username"]).first()
#     print(student)
#     if (student is not None) and bcrypt.check_password_hash(
#         student.password, request.json["password"]
#     ):
#         access_token = create_access_token(identity={'username': student.username})
#         return response_base(message="Authenticated", status=200, data=[{"token" : access_token}])
#     else:
#         return response_base(message="Incorrect credentials", status=403, data=[])


@app.route("/test-auth", methods=["POST"])
@jwt_required()
def test_auth():
    current_user = get_jwt_identity()
    return current_user
from src.database import db
from flask import request, Blueprint, jsonify, g
from src.user.model import User
from datetime import timedelta
from src.utils.error_handel import InstaCloneException
from flask_api import status
from src.utils.serializers import all_user_serializer, user_serializer
from src.utils.jwt_bearer import (
    create_access_token,
    create_refresh_token,
    token_required,
)

user_app = Blueprint("user", __name__)


@user_app.route("/sign_up", methods=["POST"])
def create_user():
    """signup user and create user"""

    user = User(**request.json)
    if User.query.filter(User.email_id == user.email_id).first():
        raise InstaCloneException(
            message="User already exist", status_code=status.HTTP_400_BAD_REQUEST
        )
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_id": user.email_id,
                "dob": user.dob,
                "country": user.country,
                "bio": user.bio,
            }
        ),
        status.HTTP_201_CREATED,
    )


@user_app.route("/sign_in", methods=["POST"])
def check_valid_user():
    """sign_in user"""

    email_id = request.json.get("email_id")
    password = request.json.get("password")

    user = User.query.filter(
        User.email_id == email_id, User.password == password
    ).first()
    if user:
        access_expire_time = timedelta(days=7)
        refresh_expire_time = timedelta(days=30)
        access_token = create_access_token(
            subject={
                "id": user.id,
                "email_id": user.email_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            expire_time=access_expire_time,
        )
        refresh_token = create_refresh_token(
            subject={
                "user_id": user.id,
                "email_id": user.email_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            expire_time=refresh_expire_time,
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, status.HTTP_200_OK
    else:
        raise InstaCloneException(
            message="Wrong email and password", status_code=status.HTTP_400_BAD_REQUEST
        )


@user_app.route("/get_all_user", methods=["GET"])
def get_all_user():
    """get all users"""

    all_user = User.query.all()
    return (
        jsonify(
            all_user_serializer(all_user),
        ),
        status.HTTP_200_OK,
    )


@user_app.route("/get_user/<user_id>", methods=["GET"])
def get(user_id):
    """get particular user"""

    user = User.query.filter(User.id == user_id).first()
    if not user:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    return jsonify(user_serializer(user)), status.HTTP_200_OK


@user_app.route("/update_user/<user_id>", methods=["PUT"])
@token_required
def partial_update(user_id):
    """update user"""

    user = User.query.filter(User.id == user_id).first()

    if "first_name" in request.json:
        user.first_name = request.json["first_name"]
    if "last_name" in request.json:
        user.last_name = request.json["last_name"]
    if "email_id" in request.json:
        user.email_id = request.json["email_id"]
    if "dob" in request.json:
        user.dob = request.json["dob"]
    if "country" in request.json:
        user.country = request.json["country"]
    if "bio" in request.json:
        user.bio = request.json["bio"]

    user.updated_by = g.user.id
    db.session.commit()

    return jsonify({"message": f"{user_id} update successfully"}), status.HTTP_200_OK


@user_app.route("/delete_user/<user_id>", methods=["DELETE"])
@token_required
def delete_user(user_id):
    """delete user"""
 
    user = User.query.filter(User.id == user_id).first()

    user.is_delete = True
    db.session.commit()

    return jsonify(
        message=f"{user_id} deleted successfully", status_code=status.HTTP_200_OK
    )

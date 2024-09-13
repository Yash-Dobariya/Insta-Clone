from flask import Blueprint, jsonify, g, request
from src.follow.model import Follow
from src.utils.jwt_bearer import token_required
from src.database import db
from flask_api import status
from src.utils.serializers import follow_details_serializer
from src.image.model import ImagePost


follow_user = Blueprint("follow_user", __name__)


@follow_user.route("/following_user/<user_id>", methods=["GET"])
@token_required
def follow_by_user(user_id):
    """user can follow another user"""

    follow = Follow.query.filter(
        Follow.follower == g.user_data.id, Follow.following == user_id
    ).first()

    if follow is None:
        follow_data = Follow(following=user_id, follower=g.user_data.id)
        db.session.add(follow_data)
        message = f"You are now following {user_id}"
    else:
        db.session.delete(follow)
        message = f"You have unfollow {user_id}"

        db.session.commit()

    return jsonify({"message": message})


@follow_user.route("/user/<user_id>/following-follower-post-count", methods=["GET"])
@token_required
def follow_counts(user_id):
    """following and followers counts"""

    image_data = ImagePost.query.filter(ImagePost.uploaded_by == user_id).count()
    following_count = Follow.query.filter(Follow.following == user_id).count()
    follower_count = Follow.query.filter(Follow.follower == user_id).count()

    return (
        jsonify(
            {
                "post": image_data,
                "following": following_count,
                "followers": follower_count,
            }
        ),
        status.HTTP_200_OK,
    )


@follow_user.route("/following/<user_id>/all_user", methods=["GET"])
@token_required
def following_users(user_id):
    """all followings users"""

    follow_data = Follow.query.filter(Follow.following == user_id).all()

    return jsonify(follow_details_serializer(follow_data, request)), status.HTTP_200_OK


@follow_user.route("/follower/<user_id>/all_user", methods=["GET"])
@token_required
def followers_users(user_id):
    """all followings users"""

    follow_data = Follow.query.filter(Follow.follower == user_id).all()
    return jsonify(follow_details_serializer(follow_data, request)), status.HTTP_200_OK

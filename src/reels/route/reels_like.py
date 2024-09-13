from flask import Blueprint, jsonify, g
from src.utils.jwt_bearer import token_required
from src.reels.model import ReelsPost
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status

like_reels = Blueprint("like_reels", __name__)


@like_reels.route("/like_reel/<reel_id>", methods=["GET"])
@token_required
def get_like(reel_id):
    """reels like"""

    reels_data = ReelsPost.query.filter(ReelsPost.id == reel_id).first()
    likes = reels_data.count_like
    liked_by = reels_data.liked_by.copy()

    """give like"""
    if liked_by is not None and g.user_data.id in liked_by:
        liked_by.remove(g.user_data.id)
        if likes > 0:
            likes -= 1
    else:
        """user take back like"""
        liked_by.append(g.user_data.id)
        likes += 1

    reels_data.count_like = likes
    reels_data.liked_by = liked_by
    db.session.commit()

    return jsonify({"like": likes, "liked_by": liked_by}), status.HTTP_200_OK

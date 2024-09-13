from flask import Blueprint, request, jsonify, g
from src.utils.jwt_bearer import token_required
from src.reels.model import ReelsPost
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status

comment_reels = Blueprint("comment_of_reels", __name__)


@comment_reels.route("/comment_reel/<reel_id>", methods=["POST"])
@token_required
def get_comments(reel_id):
    """reel_comment"""

    comment_text = request.json.get("comment")
    reels_data = ReelsPost.query.filter(ReelsPost.id == reel_id).first()

    all_comments = reels_data.comment.copy()
    new_comment = {g.user_data.id: comment_text}
    all_comments.append(new_comment)
    reels_data.comment = all_comments
    db.session.commit()

    return (
        jsonify(
            {
                "comment_text": comment_text,
                "user_id": g.user_data.id,
            }
        ),
        status.HTTP_200_OK,
    )

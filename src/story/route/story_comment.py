from flask import Blueprint, request, jsonify, g
from src.utils.jwt_bearer import token_required
from src.story.model import Story
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status

story_comments = Blueprint("comment_of_story", __name__)


@story_comments.route("/comment_story/<story_id>", methods=["POST"])
@token_required
def add_comment(story_id):
    """story comment"""

    comment_text = request.json.get("comment")
    story = Story.query.filter(Story.id == story_id).first()

    if story:
        all_comments = story.comment.copy()
        new_comment = {g.user_data.id: comment_text}
        all_comments.append(new_comment)
        story.comment = all_comments
        db.session.commit()

        return (
            jsonify(
                {
                    "comment_text": comment_text,
                    "user_id": g.user_data.id,
                },
            ),
            status.HTTP_200_OK,
        )


@story_comments.route("/user/get_comment_story/<story_id>", methods=["GET"])
@token_required
def get_user_comments(story_id):
    """get all comments of story's"""

    story = Story.query.filter(Story.id == story_id).first()

    return jsonify(
        {
            "comment_text": story.comment,
            "user_id": g.user_data.id,
        }
    )

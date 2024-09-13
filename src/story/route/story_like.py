from flask import Blueprint, jsonify, g
from src.utils.jwt_bearer import token_required
from src.story.model import Story
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status


like_story = Blueprint("like_of_story", __name__)


@like_story.route("/like_story/<story_id>", methods=["GET"])
@token_required
def get_like(story_id):
    """give story like"""

    story_data = Story.query.filter(Story.id == story_id).first()

    likes = story_data.count_like
    liked_by = story_data.liked_by.copy()

    if liked_by is not None and g.user_data.id in liked_by:
        liked_by.remove(g.user_data.id)
        if likes > 0:
            likes -= 1
    else:
        """user take_back like"""
        liked_by.append(g.user_data.id)
        likes += 1

    story_data.count_like = likes
    story_data.liked_by = liked_by
    db.session.commit()

    return (
        jsonify(
            {"like": likes, "liked_by": liked_by},
        ),
        status.HTTP_200_OK,
    )


@like_story.route("/user/story_likes/<story_id>", methods=["GET"])
@token_required
def story_likes(story_id):
    """show likes of story"""

    story_data = Story.query.filter(Story.id == story_id).first()

    return jsonify({"likes": story_data.count_like})


@like_story.route("/user/story_liked_by/<story_id>", methods=["GET"])
@token_required
def story_liked_by(story_id):
    """show all liked_by"""

    story_data = Story.query.filter(Story.id == story_id).first()

    return jsonify({"liked_by": story_data.liked_by})

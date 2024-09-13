from flask import Blueprint, request, g, jsonify
from src.utils.jwt_bearer import token_required
from src.story.high_light_story.model import HighLightStory
from src.story.model import Story
from src.database import db
from src.utils.serializers import all_highlight
from flask_api import status
from src.story.model import StoryStageMode

story_highlight = Blueprint("story_highlight", __name__)


@story_highlight.route("/user/highlight_story/<story_id>", methods=["POST"])
@token_required
def create_highlight(story_id):
    """add story in highlights"""

    uploaded_user = Story.query.filter(
        Story.id == story_id, Story.uploaded_by == g.user_data.id
    ).first()

    if uploaded_user:
        story_file = request.files["story_file"]
        highlight_name = request.form["highlight_name"]

        highlight = HighLightStory(
            add_highlight=story_file.filename,
            highlight_type=highlight_name,
            story_id=story_id,
        )

        db.session.add(highlight)
        db.session.commit()

        return {f"{story_id} in highlight"}


@story_highlight.route("/user/all_hight_lights", methods=["GET"])
@token_required
def all_highlight():
    """all highlights of user"""

    highlights = HighLightStory.query.filter(
        HighLightStory.uploaded_by == g.user_data.id
    ).all()

    if highlights:
        return {jsonify(all_highlight(highlights), status.HTTP_200_OK)}


@story_highlight.route("user_story/<story_id>")
def add_highlight_from_stage(story_id):
    """get particular story in highlight"""

    highlight_story = StoryStageMode.query.get(story_id)
    return {}

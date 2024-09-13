from flask import Blueprint, request, jsonify, g
from src.utils.jwt_bearer import token_required
from src.story.model import Story
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status
from src.story.tasks.celery_tasks import automatically_delete_story
from src.utils.serializers import story_serializer
from src.story.model import StoryStageMode
from src.story.high_light_story.model import HighLightStory


add_story = Blueprint("add_story", __name__)


@add_story.route("/upload_story", methods=["POST"])
@token_required
def upload_story():
    """Add story"""

    story_file = request.files["post_story"]
    filename = story_file.filename

    story_data = Story(add_story=filename, uploaded_by=g.user_data.id)
    db.session.add(story_data)
    db.session.commit()
    story_data_id = story_data.id

    story_staging = StoryStageMode(
        user_story=filename, uploaded_by=g.user_data.id, story_id=story_data_id
    )
    db.session.add(story_staging)
    db.session.commit()

    automatically_delete_story.apply_async(
        args=[story_data_id],
        countdown=30,
    )

    return (
        jsonify(
            {"id": story_data_id},
        ),
        status.HTTP_200_OK,
    )


@add_story.route("/user/<user_id>/all_story", methods=["GET"])
@token_required
def all_story(user_id):
    """get all story"""

    page = request.args.get("page", 1, type=int)
    story_data = Story.query.filter(Story.uploaded_by == user_id).paginate(
        page=page, per_page=10
    )

    return (
        jsonify(story_serializer(story_data)),
        status.HTTP_200_OK,
    )


@add_story.route("/del/user_story/<story_id>", methods=["DELETE"])
@token_required
def delete_story(story_id):
    """delete story from story, story stage_mode and highlight"""

    story = Story.query.filter(
        Story.id == story_id, Story.uploaded_by == g.user_data.id
    ).first()

    story_staging = StoryStageMode.query.filter(
        StoryStageMode.story_id == story_id,
        StoryStageMode.uploaded_by == g.user_data.id,
    ).first()

    story_highlight = HighLightStory.query.filter(
        HighLightStory.story_id == story_id, HighLightStory.updated_by == g.user_data.id
    ).first()

    if story:
        if story_highlight and story_staging:
            db.session.delete(story_highlight)
            db.session.delete(story_staging)
            db.session.commit()

            return jsonify(
                message="Story deleted successfully", status_code=status.HTTP_200_OK
            )
    else:
        raise InstaCloneException(
            message="Story not there", status_code=status.HTTP_404_NOT_FOUND
        )

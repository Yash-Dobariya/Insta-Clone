from src.story.tasks import celery_app
from src.story.model import Story
from src.database import db
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def automatically_delete_story(self, story_id):
    """delete story using celery"""

    story = Story.query.get(story_id)

    if story:
        db.session.delete(story)
        db.session.commit()

        logger.info("Successfully deleted story with ID: %s", story_id)

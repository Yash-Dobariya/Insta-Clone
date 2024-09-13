from src.user.route import user_app
from flask import Flask, jsonify, g, request
from dotenv import load_dotenv
import os, traceback
from src.database import db
from flask_jwt_extended import JWTManager
from src.image.route.image_upload import image_upload
from src.image.route.image_like import like_images
from src.image.route.image_comment import comment_images
from src.reels.route.reels_upload import reels_upload
from src.reels.route.reels_like import like_reels
from src.reels.route.reels_comment import comment_reels
from src.story.route.story_upload import add_story
from src.story.route.story_like import like_story
from src.story.route.story_comment import story_comments
from src.message.route.message_send import send_message
from src.follow.route.follow_following import follow_user
from src.utils.error_handel import InstaCloneException
from flask_api import status
from src.config import Config
from src.story.tasks import init_celery
from flask_socketio import SocketIO, emit
from src.utils.jwt_bearer import token_required


def create_app():
    load_dotenv()

    app = Flask(__name__)

    socketio = SocketIO(app)
    socketio.init_app(app)

    """get database url"""
    app.config.from_object(Config)

    """secret key of tokens"""
    app.config["SECRET_KEY"] = os.environ.get("SECRET")

    db.init_app(app)

    @app.teardown_appcontext
    def teardown_db(error):
        """automatically close database"""
        db.session.close()

    """register all blueprints"""
    app.register_blueprint(user_app)
    app.register_blueprint(image_upload)
    app.register_blueprint(like_images)
    app.register_blueprint(comment_images)
    app.register_blueprint(reels_upload)
    app.register_blueprint(like_reels)
    app.register_blueprint(comment_reels)
    app.register_blueprint(add_story)
    app.register_blueprint(like_story)
    app.register_blueprint(story_comments)
    app.register_blueprint(send_message)
    app.register_blueprint(follow_user)

    """initialise app in celery"""
    init_celery(app)

    """error handling"""

    @app.errorhandler(Exception)
    def handle_known_exceptions(exception: Exception):
        app.logger.error(traceback.format_exc())

        if isinstance(exception, InstaCloneException):
            return (jsonify(message=exception.message), exception.status_code)

        return (
            jsonify(message="Something went wrong!!", error=str(exception)),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    users = {}

    @socketio.on("status_update")
    @token_required
    def handle_status_update(data):
        user_id = g.user_data.id
        status = data["status"]
        users[user_id] = status

        # Emit the "status_updated" event only to the user who sent the event
        emit("status_updated", {"user_id": user_id, "status": status}, room=request.sid)

    JWTManager(app)

    return app


main_app = create_app()
celery_app = main_app.extensions["celery"]

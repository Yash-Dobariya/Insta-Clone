from flask import g
from src.user.model import User


def all_user_serializer(all_user):
    """all user serializer"""

    result = []
    for user in all_user:
        result.append(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_id": user.email_id,
                "dob": user.dob,
                "country": user.country,
            }
        )
    return result


def user_serializer(user):
    """particular user serialiser"""

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email_id": user.email_id,
        "dob": user.dob,
        "country": user.country,
        "bio": user.bio,
    }


def image_serializer(image_data):
    """Image serializer"""

    result = []
    for image in image_data:
        result.append(
            {
                "id": image.id,
                "filename": image.img_filename,
                "caption": image.caption,
                "count_like": image.count_like,
                "liked_by": image.liked_by,
                "comment": image.comment,
            }
        )
    return result


def reel_serializer(reel_data):
    """Reel serializer"""

    result = []
    for reel in reel_data:
        result.append(
            {
                "id": reel.id,
                "file_name": reel.reel_file,
                "caption": reel.caption,
                "likes": reel.count_like,
                "liked_by": reel.liked_by,
                "comment": reel.comment,
            }
        )
    return result


def story_serializer(story_data):
    """Story serializer"""

    result = []
    for story in story_data:
        result.append(
            {
                "id": story.id,
                "story": story.add_story,
                "likes": story.count_like,
                "like_by": story.liked_by,
                "comment": story.comment,
            }
        )
    return result


def message_receive_serializer(message_data):
    """message receive"""

    result = []
    for msg in message_data:
        result.append(
            {"sender_id": msg.sender_id, "message": msg.message, "sent_at": msg.send_at}
        )
    return result


def message_sending_serializer(message_data):
    """message sending"""

    result = []
    for msg in message_data:
        result.append(
            {
                "id": msg.id,
                "sender_id": msg.message_receive,
                "message": msg.message,
                "sent_at": msg.send_at,
            }
        )
    return result


def follow_details_serializer(follow_data, request):
    """Serialize follow user details"""

    result = []
    for follow in follow_data:
        if "following" in request.url:
            result.append(
                {
                    "id": follow.following,
                    "name": f"{follow.user_follower.first_name} {follow.user_follower.last_name}",
                }
            )
        elif "follower" in request.url:
            result.append(
                {
                    "id": follow.follower,
                    "name": f"{follow.user_following.first_name} {follow.user_following.last_name}",
                }
            )

    return result


def all_highlight(highlights):
    """serializer all highlight of story"""

    result = []
    for highlight in highlights:
        result.append(
            {
                "story": highlight.add_highlight,
                "highlight_type": highlight.highlight_type,
                "uploaded_by": highlight.uploaded_by,
                "story_id": highlight.story_id,
                "likes": highlight.count_likes,
            }
        )

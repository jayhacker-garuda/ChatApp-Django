from .models import PrivateChatRoom, ChatMessage, User
from typing import Optional, Dict


def serialize_private_message_model(cm: ChatMessage, user_id):
    sender_pk = cm.sender.pk
    is_out = sender_pk == user_id

    obj = {
        "text": cm.message,
        "sent": int(cm.created.timestamp()),
        "edited": int(cm.modified.timestamp()),
        "read": cm.read,
        "sender": str(sender_pk),
        "recipient": str(cm.recipient.pk),
        "out": is_out,
        "sender_username": cm.sender.get_username()
    }

    return obj


def serialize_private_room_model(pcr: PrivateChatRoom, user_id):
    username_field = User.USERNAME_FIELD

    other_user_pk, other_user_username = User.objects.filter(pk=pcr.user1.pk).values_list('pk', username_field).first()\
        if pcr.user2.pk == user_id else User.objects.filter(pk=pcr.user2.pk).values_list('pk', username_field).first()
    
    unread_count = ChatMessage.get_unread_count_for_private_chat_with_user(sender=other_user_pk,recipient=user_id)
    last_message: Optional[ChatMessage] = ChatMessage.get_last_message_for_private_chat(sender=other_user_pk,recipient=user_id)
    
    last_message_ser = serialize_private_message_model(last_message,user_id) if last_message else None
    
    obj = {
        "created": int(pcr.created.timestamp()),
        "modified": int(pcr.modified.timestamp()),
        "other_user_id":str(other_user_pk),
        "unread_count": unread_count,
        "username": other_user_username,
        "last_message": last_message_ser
    }
    
    return obj

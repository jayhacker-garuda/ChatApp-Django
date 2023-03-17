from channels.db import database_sync_to_async
from private_chat.models import ChatMessage, PrivateChatRoom as Private,User
from typing import Set, Awaitable, Optional, Tuple
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



@database_sync_to_async
def get_groups_to_add(u:AbstractUser)-> Awaitable[Set[int]]:
    l = Private.get_private_chat_for_user(u)
    print(set(list(sum(l, ()))))
    return set(list(sum(l,())))


@database_sync_to_async
def get_user_by_pk(pk:str)-> Awaitable[Optional[AbstractUser]]:
    return User.objects.filter(pk=pk).first()

@database_sync_to_async
def get_message_by_id(mid:int)-> Awaitable[Optional[Tuple[str,str]]]:
    msg: Optional[ChatMessage] = ChatMessage.objects.filter(id=mid).first()
    
    if msg:
        return str(msg.recipient.pk), str(msg.sender.pk)
    else: 
        return None


@database_sync_to_async
def mark_message_as_read(mid: int) -> Awaitable[None]:
    return ChatMessage.objects.filter(id=mid).update(read=True)


@database_sync_to_async
def get_unread_count(sender,recipient) -> Awaitable[int]:
    return int(ChatMessage.get_unread_count_for_private_chat_with_user(sender,recipient))


@database_sync_to_async
def save_text_message(text:str,_from:AbstractUser,to:AbstractUser) -> Awaitable[ChatMessage]:
    return ChatMessage.objects.create(message=text,sender=_from,recipient=to)
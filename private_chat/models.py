from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags import humanize
from django.template.defaultfilters import slugify
from core.models import BaseModel

from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime
from model_utils.models import TimeStampedModel, SoftDeletableModel, SoftDeletableManager
from typing import Optional, Any
# from chat.models import Room


User: AbstractUser = get_user_model()
# Create your models here.


class PrivateChatRoom(BaseModel, TimeStampedModel):
    user1 = models.ForeignKey(
        to=User, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_("User1"),
        related_name="+", db_index=True
    )
    user2 = models.ForeignKey(
        to=User, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_("User2"),
        related_name="+", db_index=True
    )

    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))
        verbose_name = _("Private_Chat")
        verbose_name_plural = _("Private_Chats")

    def __str__(self):
        return _("Private chat between") + f'{self.user1.username},{self.user2.username}'

    # def save(self, *args, **kwargs):
    #     self.name = slugify(self.name)
    #     super(PrivateChatRoom, self).save(*args, **kwargs)

    # @staticmethod
    # def room_exists(room_name: Any) -> Optional[Any]:
    #     return PrivateChatRoom.objects.filter(Q(name__iexact=room_name)).first()

    # @staticmethod
    # def create_room_if_not_existss(self,room_name):
    #     room = self.room_exist(room_name)

    #     if not room:
    #         PrivateChatRoom.o

    @staticmethod
    def private_chat_exists(u1: AbstractUser, u2: AbstractUser) -> Optional[Any]:
        return PrivateChatRoom.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: AbstractUser, u2: AbstractUser):
        res = PrivateChatRoom.private_chat_exists(u1, u2)

        if not res:
            PrivateChatRoom.objects.create(user1=u1, user2=u2)
        # return res

    @staticmethod
    def get_private_chat_for_user(user: AbstractUser):
        return PrivateChatRoom.objects.filter(Q(user1=user) | Q(user2=user)).values_list('user1__pk', 'user2__pk')


class ChatMessage(BaseModel, TimeStampedModel, SoftDeletableModel):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_(
        "Author"), related_name='from_user', db_index=True)
    recipient = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_(
        "Recipient"), related_name='to_user', db_index=True)
    message = models.TextField(
        max_length=512, verbose_name=_("Message"), blank=True
    )
    read = models.BooleanField(verbose_name=_("Read"), default=False)

    all_objects = models.Manager()

    class Meta:
        ordering = ('created',)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self) -> str:
        return f'{self.user.username}: {self.message} [{self.created_at}]'

    @staticmethod
    def get_unread_count_for_private_chat_with_user(sender, recipient):
        return ChatMessage.objects.filter(sender_id=sender, recipient_id=recipient, read=False).count()

    @staticmethod
    def get_last_message_for_private_chat(sender, recipient):
        return ChatMessage.objects.filter(
            Q(sender_id=sender, recipient_id=recipient) | Q(
                sender_id=sender, recipient_id=recipient)
        ).select_related('sender', 'recipient').first()

    def save(self, *args, **kwargs):
        super(ChatMessage, self).save(*args, **kwargs)
        PrivateChatRoom.create_if_not_exists(self.sender, self.recipient)

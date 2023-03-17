from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import serialize_private_message_model, serialize_private_room_model
from django.db.models import Q
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView,

)
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import Page, Paginator
from django.conf import settings

from .models import PrivateChatRoom, ChatMessage
from django.contrib.auth import get_user_model
# from django.forms import ModelForm
# import json


# Create your views here.

class PrivateChatView(LoginRequiredMixin, View):
    template_name = 'private_chat/room.html'

    def get(self, request, *args, **kwargs):

        temp_name = '{0}-{1}'.format(kwargs.get('me'), kwargs.get('username'))
        private_room, created = PrivateChatRoom.objects.get_or_create(
            name=temp_name
        )

        private_messages = ChatMessage.objects.filter(room=private_room)[0:25]

        return render(request, self.template_name, {
            'private_chat_room': private_room,
            'private_messages': private_messages
        })


class UserInboxList(LoginRequiredMixin,ListView):
    template_name = 'private_chat/users.html'
    model = get_user_model()
    context_object_name = 'users'
    

class MessagesRoom(LoginRequiredMixin, ListView):
    template_name = 'private_chat/_message_room.html'
    http_method_names = ['get', ]
    paginate_by = getattr(settings, 'MESSAGES_PAGINATION', 500)

    def get_queryset(self):
        if self.kwargs.get('dialog_with'):
            qs = ChatMessage.objects \
                .filter(Q(recipient=self.request.user, sender=self.kwargs['dialog_with']) |
                        Q(sender=self.request.user, recipient=self.kwargs['dialog_with'])) \
                .select_related('sender', 'recipient')
        else:
            qs = ChatMessage.objects.filter(Q(recipient=self.request.user) |
                                            Q(sender=self.request.user)).prefetch_related('sender', 'recipient',)

        return qs.order_by('created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.request.user.pk
        data = [serialize_private_message_model(i, user_pk)
                for i in context['object_list']]
        page: Page = context.pop('page_obj')
        paginator: Paginator = context.pop('paginator')

        context = {
            "page": page.number,
            'pages': paginator.num_pages,
            'data': data
        }

        print(context)
        return context

# class MessagesModelList(LoginRequiredMixin, ListView):
#     template_name = 'private_chat/message_list.html'
#     http_method_names = ['get', ]
#     paginate_by = getattr(settings, 'MESSAGES_PAGINATION', 500)

#     def get_queryset(self):


#         return qs.order_by('-created')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_pk = self.request.user.pk
    #     data = [serialize_private_message_model(i, user_pk)
    #             for i in context['object_list']]
    #     page: Page = context.pop('page_obj')
    #     paginator: Paginator = context.pop('paginator')

    #     context = {
    #         "page": page.number,
    #         'pages': paginator.num_pages,
    #         'data': data
    #     }

    #     print(context)
    #     return context
    # def render_to_response(self, context, **response_kwargs):
    #     user_pk = self.request.user.pk
    #     data = [serialize_private_message_model(i, user_pk)
    #             for i in context['object_list']]
    #     page: Page = context.pop('page_obj')
    #     paginator: Paginator = context.pop('paginator')
    #     return_data = {
    #         'page': page.number,
    #         'pages': paginator.num_pages,
    #         'data': data
    #     }
    #     return JsonResponse(return_data, **response_kwargs)


class DialogsModelList(LoginRequiredMixin, ListView):
    # template_name = 'private_chat/message_list.html'
    template_name = 'private_chat/dialogs_list.html'
    http_method_names = ['get', ]
    paginate_by = getattr(settings, 'DIALOGS_PAGINATION', 20)

    def get_queryset(self):
        qs = PrivateChatRoom.objects.filter(Q(user1_id=self.request.user.pk) | Q(user2_id=self.request.user.pk)) \
            .select_related('user1', 'user2')
        return qs.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.request.user.pk
        data = [serialize_private_room_model(i, user_pk)
                for i in context['object_list']]
        page: Page = context.pop('page_obj')
        paginator: Paginator = context.pop('paginator')

        context = {
            "page": page.number,
            'pages': paginator.num_pages,
            'data': data
        }

        print("Line 117 Dialog {}".format(context))
        return context
    # def render_to_response(self, context, **response_kwargs):
    #     # TODO: add online status
    #     user_pk = self.request.user.pk
    #     data = [serialize_private_room_model(i, user_pk)
    #             for i in context['object_list']]
    #     page: Page = context.pop('page_obj')
    #     paginator: Paginator = context.pop('paginator')
    #     return_data = {
    #         'page': page.number,
    #         'pages': paginator.num_pages,
    #         'data': data
    #     }
    #     return JsonResponse(return_data, **response_kwargs)


class SelfInfoView(LoginRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        return self.request.user

    def render_to_response(self, context, **response_kwargs):
        user: AbstractUser = context['object']
        data = {
            "username": user.get_username(),
            "pk": str(user.pk)
        }
        return JsonResponse(data, **response_kwargs)

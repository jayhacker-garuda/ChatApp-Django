from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Room, Message
from .forms import CreateRoomForm

# Create your views here.


class ChatHome(LoginRequiredMixin, View):
    template_name = 'chat/index.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {
            'rooms': Room.objects.all(),
        })


class ChatRoomCreate(LoginRequiredMixin, View):
    template_name = 'chat/room/create_chat_room.html'
    _RoomForm = CreateRoomForm
    redirect_link = reverse_lazy('chat:index')

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {'room_form': self._RoomForm})

    def post(self, request, *args, **kwargs):

        tempForm = self._RoomForm(request.GET)
        valid_Form = self._RoomForm(request.POST)

        if valid_Form.is_valid():
            valid_Form.save(commit=True)
            return redirect(self.redirect_link)

        return render(request, self.template_name, {'room_form': tempForm})


class ChatRoom(LoginRequiredMixin, View):
    template_name = 'chat/room/chat_room.html'

    def get(self, request, *args, **kwargs):
        chat_room = Room.objects.get(
            slug=kwargs.get('room_name')
        )
        # print(created)
        if chat_room:
            chat_messages = Message.objects.filter(room=chat_room)[0:25]

            return render(request, self.template_name, {
                'room_name': chat_room,
                'chat_messages': chat_messages
            })
        return render(request, self.template_name, {
            'room_name': chat_room,
            'chat_messages': []
        })

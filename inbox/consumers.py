from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
import json
from asgiref.sync import async_to_sync
from .models import *
from django.template.loader import render_to_string

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.chatroom = get_object_or_404(Conversation, id=self.conversation_id)

        async_to_sync (self.channel_layer.group_add)(
            self.conversation_id,
            self.channel_name
        )

        #add and update the online users
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync (self.channel_layer.group_discard)(
            self.conversation_id,
            self.channel_name
        )

        #remove and update the online users
        if self.user  in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = InboxMesssage.objects.create(
            sender=self.user, 
            conversation=self.chatroom, 
            body=body
            )
        event =  {
              'type': 'message_handler',
              'message_id': message.id,
        }
        async_to_sync (self.channel_layer.group_send)(
            self.conversation_id,
            event
        )
    
    def message_handler(self, event):
        message_id = event['message_id']
        message = InboxMesssage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,  
            'conversation': self.chatroom
        }
        html = render_to_string('inbox/partials/chat_message.html', context=context)
        self.send(text_data=json.dumps({
            'html': html,
            'message_id': message_id
        }))

    def update_online_count(self):
        online_count = self.chatroom.users_online.count()

        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }

        async_to_sync (self.channel_layer.group_send)(self.conversation_id,event)

    def online_count_handler(self, event):
        online_count = event['online_count']
        context = {
            'online_count': online_count,
            'conversation': self.chatroom,
            'user': self.user
        }
        html = render_to_string('inbox/partials/online_count.html', context=context)
        self.send(text_data=json.dumps({
            'type': 'online_count',
            'html': html
        }))

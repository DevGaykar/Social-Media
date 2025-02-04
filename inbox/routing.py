from django.urls import path
from  .consumers import * 

websocket_urlpatterns = [
    path('ws/inbox/<str:conversation_id>/', ChatroomConsumer.as_asgi()),
]
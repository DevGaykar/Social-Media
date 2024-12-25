from django.urls import path
from .views import *

app_name = 'inbox'

urlpatterns = [
    path('', inbox_view,name="inbox"),
    path('c/<conversation_id>/',inbox_view,name="inbox"),
    path('start_conversation/<str:username>/', start_conversation, name='start_conversation'),
    path('<str:conversation_id>/send/', send_message, name='send_message'),
]

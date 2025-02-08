from django.urls import path
from .views import *

app_name = 'inbox'

urlpatterns = [
    path('', inbox_view, name="inbox"),
    path('c/<conversation_id>/', inbox_view, name="inbox"),
    path('start_conversation/<str:username>/', start_conversation, name='start_conversation'),
    path('start_conversation/<str:username>/<str:conversation_type>/', start_conversation, name='start_conversation_with_type'),
    path('start_group_conversation/', start_group_conversation, name='start_group_conversation'),
    path('world_chat/', world_chat_view, name='world_chat'),
    path('send-message/<uuid:conversation_id>/', send_message, name='send_message'),
    path('file-upload/<str:conversation_id>/', send_file, name='send_file'),
    path('add-participants/<str:conversation_id>/', add_participants, name='add_participants'),
    path('make-admin/<str:conversation_id>/<int:user_id>/', make_admin, name='make-admin'),
    path('remove-participant/<str:conversation_id>/<int:user_id>/', remove_participant, name='remove-participant'),
    path('delete-group/<str:conversation_id>/', delete_group, name='delete-group'),
    path('edit-group/<str:conversation_id>/', edit_group, name='edit-group'),
    
]

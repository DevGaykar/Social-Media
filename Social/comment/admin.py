from django.contrib import admin
from .models import Comment, Reply,LikedComment,LikedReply

admin.site.register(Comment)
admin.site.register(LikedComment)
admin.site.register(Reply)
admin.site.register(LikedReply)
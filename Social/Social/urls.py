"""
URL configuration for Social project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from userauths.views import UserProfile,follow
from comment.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
     path('accounts/', include('allauth.urls')),
    path('',include('post.urls')),
    path('user/',include('userauths.urls')),

    #profile
    path('<username>/',UserProfile,name='profile'),
    path('<username>/saved/',UserProfile,name='profilefavourite'),
    path('<username>/follow/<option>/',follow,name='follow'),

    #comment
    path('commentsent/<post_id>/', comment_sent, name='comment-sent'), 
    path('comment/delete/<pk>/',comment_delete_view,name="comment-delete"),
    path('comment/like/<post_id>/',like_comment,name="like-comment"),
    path('reply-sent/<post_id>/' , reply_sent, name='reply-sent'),
    path('reply/delete/<pk>/',reply_delete_view,name="reply-delete"),
    path('reply/like/<post_id>/',like_reply,name="like-reply"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
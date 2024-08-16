from  django.contrib import admin
from django.urls import path
from post import views
urlpatterns = [
    path('',views.home,name='home'),
    path('newpost',views.NewPost,name='newpost'),
    path('<uuid:post_id>',views.PostDetail,name='post-details'),
    path('tag/<slug:tag_slug>',views.Tags,name='tags'),
]
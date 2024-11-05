from  django.contrib import admin
from django.urls import path
from post import views
urlpatterns = [
    path('',views.home,name='home'),
    path('newpost/',views.NewPost,name='newpost'),
    path('<uuid:post_id>',views.PostDetail,name='post-details'),
    path('<uuid:post_id>/delete/',views.PostDelete,name='delete-post'),
    path('tag/<slug:tag_slug>',views.Tags,name='tags'),
    path('<uuid:post_id>/like',views.like_post,name='like-post'),
    path('<uuid:post_id>/favourite',views.favourite,name='favourite'),
]
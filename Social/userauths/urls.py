from django.urls import path
from . import views
from userauths.views import UserProfile, EditProfile

urlpatterns = [
    path('profile/edit',EditProfile,name="editprofile"),
]
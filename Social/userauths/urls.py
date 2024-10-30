from django.urls import path
from . import views
from userauths.views import *

urlpatterns = [
    path('profile/edit/',EditProfile,name="editprofile"),
    path('profile/delete/',DeleteProfile,name="deleteprofile"),
]
from django.urls import path
from . import views
from userauths.views import *

urlpatterns = [
    path('edit/',EditProfile,name="editprofile"),
    path('profile/delete/',DeleteProfile,name="deleteprofile"),
    path('profile/onboarding/',DeleteProfile,name="profile-onboarding"),
    path('settings/',Settings,name="settings"),
    # path('start_conversation/<str:username>/', views.start_conversation, name='start_conversation'),
]
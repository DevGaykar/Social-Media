from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from django.templatetags.static import static
from cloudinary_storage.storage import MediaCloudinaryStorage
from django_resized import ResizedImageField

def profile_picture_path(instance, filename):
    # Creates path like: media/user_1/profile_pictures/filename
    return f'media/user_{instance.user.id}/profile_pictures/{filename}'

def header_image_path(instance, filename):
    # Creates path like: media/user_1/header_images/filename
    return f'media/user_{instance.user.id}/header_images/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = ResizedImageField(size=[600,600],quality=85,upload_to=profile_picture_path, storage=MediaCloudinaryStorage(),null=True,blank=True)
    header_image = ResizedImageField(size=[1500,500],quality=85,crop=['middle', 'center'],upload_to=header_image_path, storage=MediaCloudinaryStorage(),null=True,blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    favourite = models.ManyToManyField(Post,blank=True)
    email = models.EmailField(unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f'{self.user.username} - Profile'
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('/images/avatar_default.png') 
            print(f"Using default avatar: {avatar}")
        return avatar
    
    @property
    def name(self):
        if self.first_name and self.last_name:
            name = f"{self.first_name} {self.last_name}"
        else:
            name = self.user.username 
        return name
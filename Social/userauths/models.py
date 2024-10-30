from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_picture", null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    favourite = models.ManyToManyField(Post,blank=True)

    def __str__(self) :
        return f'{self.user.username} - Profile'
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('/profile_picture/avatar_default.png') 
            print(f"Using default avatar: {avatar}")
        return avatar
    
    @property
    def name(self):
        if self.first_name and self.last_name:
            name = f"{self.first_name} {self.last_name}"
        else:
            name = self.user.username 
        return name
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage
import pytz

#Uploading user files to a secific directory
def user_directory_path(instance,filename):
     # Creates path like: media/user_1/story/filename
    return f'media/user_{instance.user.id}/story/{filename}'

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=user_directory_path,storage=MediaCloudinaryStorage())
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'

    def save(self, *args, **kwargs):
        # Always set expiration to 24 hours from now when creating
        if not self.pk or not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def content_type(self):
        extension = self.content.name.lower()
        if extension.endswith(('.mp4', '.mov')):
            return 'video'
        return 'photo'

    def __str__(self):
        ist = pytz.timezone('Asia/Kolkata')
        ist_time = self.expires_at.astimezone(ist)
        formatted_time = ist_time.strftime('%Y-%m-%d %I:%M %p IST')
        return f'Story by {self.user.username} - Expires {formatted_time}'

class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'viewer')
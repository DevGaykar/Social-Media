import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timesince import timesince
from cryptography.fernet import Fernet
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary_storage.storage import MediaCloudinaryStorage
from django_resized import ResizedImageField

def group_profile_path(instance, filename):
    """
    Generate the upload path for group profile images.
    Format: group_images/{group_id}/{filename}
    """
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a clean filename using group name and id
    clean_filename = f"{instance.group_name}_{instance.id}.{ext}"
    # Return the complete path
    return f'group_images/{instance.id}/{clean_filename}'

class InboxMesssage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")
    conversation = models.ForeignKey('Conversation',on_delete=models.CASCADE,related_name="messages")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def body_decrypted(self):
        f = Fernet(settings.ENCRYPT_KEY)
        message_decrypted = f.decrypt(self.body)
        message_decode = message_decrypted.decode('utf-8')
        return message_decode

    @classmethod
    def create_message(cls, sender, conversation, body):
        if conversation.type == 'world':
            # Handle world chat message creation
            for user in User.objects.all():
                if not cls.objects.filter(sender=sender, conversation=conversation, body=body).exists():
                    cls.objects.create(sender=sender, conversation=conversation, body=body)
        else:
            # Handle one-to-one and group chat message creation
            if not cls.objects.filter(sender=sender, conversation=conversation, body=body).exists():
                cls.objects.create(sender=sender, conversation=conversation, body=body)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        time_since = timesince(self.created, timezone.now())
        return f'[{self.sender.username} : {time_since} ago]'

class Conversation(models.Model):
    CONVERSATION_TYPE_CHOICES = [
        ('one_to_one', 'One to One'),
        ('group', 'Group'),
        ('world', 'World'),
    ]
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    lastmessage_created = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=CONVERSATION_TYPE_CHOICES, default='one_to_one')
    group_name = models.CharField(max_length=100, blank=True, null=True)  # Add group_name field
    group_image = ResizedImageField(
        size=[600,600],quality=75,
        upload_to=group_profile_path,
        storage=MediaCloudinaryStorage(), 
        null=True, 
        blank=True
    )
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='administered_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_formatted_date(self):
        return self.created_at.strftime("%B %d, %Y")

    class Meta:
        ordering = ['-lastmessage_created']

    def __str__(self):
        user_names = ", ".join(user.username for user in self.participants.all())
        return f'[{self.type} - {user_names}]'

@receiver(post_save, sender=User)
def add_user_to_world_chat(sender, instance, created, **kwargs):
    if created:
        world_chat, created = Conversation.objects.get_or_create(type='world')
        if created:
            world_chat.participants.set(User.objects.all())
            world_chat.save()

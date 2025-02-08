from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

f = Fernet(settings.ENCRYPT_KEY)

@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    conversation = None
    context = {
        'conversation': None,
        'my_conversations': my_conversations,
        'form': GroupConversationForm()
    }
    
    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
        context['conversation'] = conversation
        if conversation.type == 'group':
            available_users = User.objects.exclude(id__in=conversation.participants.all())
            context['available_users'] = available_users
    
    return render(request, 'inbox/inbox.html', context)

@login_required
def start_conversation(request, username=None, conversation_type='one_to_one'):
    if conversation_type == 'world':
        conversation, created = Conversation.objects.get_or_create(type='world')
        if created:
            conversation.participants.set(User.objects.all())
            conversation.save()
    elif conversation_type == 'group':
        group_name = request.POST.get('group_name', 'Unnamed Group')
        conversation = Conversation.objects.create(type='group', group_name=group_name)
        conversation.participants.add(request.user)
        conversation.save()
    else:
        other_user = get_object_or_404(User, username=username)
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).first()
        
        if conversation is None:
            conversation = Conversation.objects.create(type=conversation_type)
            conversation.participants.add(request.user, other_user)
            conversation.save()
    
    return redirect('inbox:inbox', conversation_id=conversation.id)

@login_required
def start_group_conversation(request):
    if request.method == 'POST':
        form = GroupConversationForm(request.POST, request.FILES)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.type = 'group'
            conversation.admin = request.user  # Set the creator as admin
            conversation.save()
            conversation.participants.add(request.user)  # Add creator to participants
            conversation.participants.add(*form.cleaned_data['participants'])
            return redirect('inbox:inbox', conversation_id=conversation.id)
    return redirect('inbox:inbox')

@login_required
def world_chat_view(request):
    world_chat, created = Conversation.objects.get_or_create(type='world')
    if created:
        world_chat.participants.set(User.objects.all())
        world_chat.save()
    else:
        # Ensure all users are participants in the world chat
        all_users = User.objects.all()
        for user in all_users:
            if user not in world_chat.participants.all():
                world_chat.participants.add(user)
        world_chat.save()
    return redirect('inbox:inbox', conversation_id=world_chat.id)

@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Verify user is a participant in the conversation
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        message_body =  request.POST.get('body')
        if message_body:
            message = InboxMesssage.objects.create(
                sender=request.user,
                conversation=conversation,
                body=message_body
            )
            conversation.lastmessage_created = timezone.now()
            conversation.save()
            return render(request,'inbox/partials/chat_message.html',context={'message':message,'request':request})
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def send_file(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Verify user is a participant in the conversation
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = InboxMesssage.objects.create(
            sender=request.user,
            conversation=conversation,
            file=file
        )
        conversation.lastmessage_created = timezone.now()
        conversation.save()

        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(
            conversation_id, event
        )
    return HttpResponse()

@login_required
def add_participants(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.admin:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        new_participant_ids = request.POST.getlist('new_participants')
        new_participants = User.objects.filter(id__in=new_participant_ids)
        conversation.participants.add(*new_participants)
        return redirect('inbox:inbox', conversation_id=conversation_id)
    return redirect('inbox:inbox')

@login_required
def make_admin(request, conversation_id, user_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.admin:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    new_admin = get_object_or_404(User, id=user_id)
    if new_admin in conversation.participants.all():
        conversation.admin = new_admin
        conversation.save()
    return JsonResponse({'status': 'success'})

@login_required
def remove_participant(request, conversation_id, user_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.admin:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    participant = get_object_or_404(User, id=user_id)
    if participant != conversation.admin:
        conversation.participants.remove(participant)
    return JsonResponse({'status': 'success'})

@login_required
def delete_group(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.admin:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    conversation.delete()
    return redirect('inbox:inbox')  # Redirect to the inbox without specifying a conversation ID

@login_required
def edit_group(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        if 'group_name' in request.POST:
            conversation.group_name = request.POST['group_name']
        if 'group_image' in request.FILES:
            conversation.group_image = request.FILES['group_image']
        conversation.save()
        return redirect('inbox:inbox', conversation_id=conversation_id)
    return redirect('inbox:inbox')
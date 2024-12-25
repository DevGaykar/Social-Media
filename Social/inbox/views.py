from django.http import JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def inbox_view(request,conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(my_conversations,id=conversation_id)
    else:
        conversation = None
    context = {
        'conversation' : conversation,
        'my_conversations':my_conversations
    }
    return render(request,'inbox/inbox.html',context)

@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Find existing conversation or create new one
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if conversation is None:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        conversation.save()
    
    # Redirect to inbox with the conversation ID
    return redirect('inbox:inbox', conversation_id=conversation.id)

@login_required
def send_message(request, conversation_id):
    """Handle sending new messages in a conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Verify user is a participant in the conversation
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        message_body = request.POST.get('body')
        
        if message_body:
            # Create new message
            message = InboxMesssage.objects.create(
                sender=request.user,
                conversation=conversation,
                body=message_body
            )
            
            # Update conversation last message time
            conversation.lastmessage_created = timezone.now()
            conversation.is_seen = False
            conversation.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return JSON response for AJAX requests
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'body': message.body,
                        'sender': request.user.username,
                        'created': message.created.isoformat(),
                    }
                })
            
            return redirect('inbox:inbox', conversation_id=conversation_id)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)
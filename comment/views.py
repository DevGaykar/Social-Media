from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
import re
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from post.views import like_toggle
from .models import Comment,Reply
from .forms import CommentCreateForm,ReplyCreateForm
from post.models import Post 
from django.contrib import messages
from django.contrib.auth.models import User
from notifications.signals import notify

@login_required
def comment_sent(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            if request.user != post.user:
                notify.send(
                sender=request.user,
                recipient=post.user,
                verb="commented on your post",
                target=post,
                action_object=comment,  
                description=comment.body[:30]  
            )
            mentions = re.findall(r'@(\w+)', comment.body)
            for username in mentions:
                try:
                    user = User.objects.get(username=username)
                    if user != request.user:  # Don't notify self-mentions
                        notify.send(
                            sender=request.user,
                            recipient=user,
                            verb="mentioned you in a comment",
                            target=post,
                            action_object=comment
                        )
                except User.DoesNotExist:
                    pass
            # Redirect to the same post detail page after saving the comment
            return redirect(reverse('post-details', args=[post.id]))  

    else:
        form = CommentCreateForm()  # Initialize an empty form for GET requests

    # Fetch existing comments related to the post
    comments = Comment.objects.filter(parent_post=post)

    context = {
        'post': post,
        'form': form,
        'comments': comments  # Use the correct variable name for comments
    }

    return render(request, 'post/post-details.html', context)

@login_required
@like_toggle(Comment)
def like_comment(request,comment,liked):
    if liked and request.user != comment.author:
        notify.send(
            sender=request.user,
            recipient=comment.author,
            verb="liked your comment",
            target=comment.parent_post,
            action_object=comment,
            description=comment.body[:30]
        )
    return render(request,'snippets/comment_like.html', {'comment': comment})

@login_required
@like_toggle(Reply)
def like_reply(request,reply,liked):
    if liked and request.user != reply.author:
        notify.send(
            sender=request.user,
            recipient=reply.author,
            verb="liked your reply",
            target=reply.parent_comment,
            action_object=reply,
            description=reply.body[:30]
        )
    return render(request,'snippets/reply_like.html', {'reply': reply})

@login_required
def reply_sent(request, post_id):
    comment = get_object_or_404(Comment, id=post_id)

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment  = comment
            reply.save()
            # Redirect to the same post detail page after saving the comment
            if request.user != comment.author:  # Avoid self-notification
                notify.send(
                    sender=request.user,
                    recipient=comment.author,
                    verb="replied to your comment",
                    target=comment.parent_post,  
                    action_object=reply,
                    description=reply.body[:30]  
                )

            mentions = re.findall(r'@(\w+)', reply.body)
            for username in mentions:
                try:
                    user = User.objects.get(username=username)
                    if user != request.user:  # Don't notify self-mentions
                        notify.send(
                            sender=request.user,
                            recipient=user,
                            verb="mentioned you in a reply",
                            target=comment.parent_post,
                            action_object=reply
                        )
                except User.DoesNotExist:
                    pass
            return redirect(reverse('post-details', args=[comment.parent_post.id]))  
    else:
        form = CommentCreateForm()  # Initialize an empty form for GET requests

    # Fetch existing comments related to the post
    replies = Reply.objects.filter(parent_comment=comment)
    context = {
        'comment': comment,
        'form': form,
         'replies' : replies,
        }

    return render(request, 'post/post-details.html', context)

@login_required
def comment_delete_view(request,pk):
    post = get_object_or_404(Comment,id=pk,author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request,'Comment deleted')
        return redirect('post-details',post.parent_post.id)

@login_required
def reply_delete_view(request,pk):
    reply = get_object_or_404(Reply,id=pk,author=request.user)

    if request.method == "POST":
        reply.delete()
        messages.success(request,'Reply deleted')
        return redirect('post-details',reply.parent_comment.parent_post.id)
    
    
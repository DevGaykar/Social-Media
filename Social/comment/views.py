from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Comment
from .forms import CommentCreateForm
from post.models import Post 

def comment_sent(request,post_id):
    post = get_object_or_404(Post, id=post_id) 
    # comment = Comment.objects.filter(parent_post=post)

    if request.method =='POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    context = {
        'post' : post,
        'form' : form,
        'comment' : comment
    }

    return render(request, 'post/post-details.html', context)
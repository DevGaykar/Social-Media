from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Comment
from .forms import CommentCreateForm
from post.models import Post 
from django.contrib import messages

# def comment_sent(request,post_id):
#     post = get_object_or_404(Post, id=post_id) 
#     # comment = Comment.objects.filter(parent_post=post)

#     if request.method =='POST':
#         form = CommentCreateForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.parent_post = post
#             comment.save()
#     context = {
#         'post' : post,
#         'form' : form,
#         'comment' : comment
#     }

#     return render(request, 'post/post-details.html', context)

def comment_sent(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
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

def comment_delete_view(request,pk):
    post = get_object_or_404(Comment,id=pk,author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request,'Comment deleted')
        return redirect('post-details',post.parent_post.id)
    
    
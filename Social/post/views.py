from userauths.models import Profile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import  login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

from post.models import Tag,Stream,Follow,Post,Likes
from django.contrib.auth.models import User
from post.forms import NewPostForm
from comment.forms import CommentCreateForm,ReplyCreateForm


def home(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context = {
        'post_items' : post_items
    }
    return render(request,"index.html",context)

def NewPost(request):
    user = request.user
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tag.set(tags_obj)
            p.save()
            return redirect('home')
    else:
        form = NewPostForm()
    context = {
        'form': form
    }
    return render(request, 'post/newpost.html', context)

def PostDetail(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    context ={
        'post':post,
        'commentform' : commentform,
        'replyform' : replyform
    }
    return render(request,'post/post-details.html',context)
    

def Tags(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    posts = Post.objects.filter(tag=tag).order_by('-posted')

    context={
        'posts' : posts,
        'tag' : tag
    }   
    return render(request,'post/tag.html',context)

# def like(request, post_id):
#     user = request.user
#     post = get_object_or_404(Post, id=post_id)

#     liked = Likes.objects.filter(user=user, post=post).first()

#     if liked:
#         liked.delete()
#         # post.likes -= 1
#         liked_status = False
#     else:
#         Likes.objects.create(user=user, post=post)
#         # post.likes += 1
#         liked_status = True

#     post.likes = post.post_likes.count()
#     post.save()

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return JsonResponse({'likes_count': post.likes, 'liked_status': liked_status})

#     return redirect('post_detail', post_id=post_id)

def like_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    user_exist = post.likes.filter(id=request.user.id).exists()

    if user_exist:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return render(request,'snippets/action-buttons.html', {'post': post})

def favourite(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    profile = get_object_or_404(Profile, user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
        saved = False
    else:
        profile.favourite.add(post)
        saved = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         return JsonResponse({'saved': saved})

    return redirect('post-details', post_id=post_id)
        
  
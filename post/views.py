from django.utils import timezone
from story.models import Story
from userauths.models import Profile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import  login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from notifications.signals import notify

from post.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from post.forms import NewPostForm,PostEditForm,PostReportForm
from comment.forms import CommentCreateForm,ReplyCreateForm
from comment.models import Comment


import json

@login_required(login_url='account_login')
def home(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    suggested_users = User.objects.exclude(id__in=followed_users).exclude(id=request.user.id)
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    stories_list = []
    print("\n=== Processing stories ===")

     # Get user's own stories
    user_stories = Story.objects.filter(
        user=request.user,
        expires_at__gt=timezone.now()
    ).order_by('-created_at')
    
    if user_stories.exists():
        items = []
        for story in user_stories:
            items.append({
                'id': str(story.id),
                'type': story.content_type(),
                'length': 3,
                'src': request.build_absolute_uri(story.content.url),
                'preview': request.build_absolute_uri(story.content.url),
                'link': '',
                'linkText': '',
                'time': int(story.created_at.timestamp() * 1000),
                'canDelete': True,  
            })
            
        stories_list.append({
            'id': str(request.user.id),
            'photo': request.user.profile.avatar,
            'name' : 'Your Story',
            'link': '',
            'lastUpdated': int(user_stories.first().created_at.timestamp() * 1000),
            'items': items
        })
    
    # Get all active stories from followed users in a single query
    active_stories = Story.objects.select_related('user', 'user__profile').filter(
        user__in=Follow.objects.filter(follower=request.user).values_list('following', flat=True), 
        expires_at__gt=timezone.now()
    ).order_by('user', '-created_at')
    
    # Group stories by user
    user_stories = {}
    for story in active_stories:
        if story.user_id not in user_stories:
            user_stories[story.user_id] = {
                'user': story.user,
                'stories': []
            }
        user_stories[story.user_id]['stories'].append(story)
    
    # Format the stories data
    for user_id, data in user_stories.items():
        user = data['user']
        items = []
        
        for story in data['stories']:
            created_timestamp = int(story.created_at.timestamp() * 1000)

            items.append({
                'id': str(story.id),
                'type': story.content_type(),
                'length': 3,
                'src': request.build_absolute_uri(story.content.url),
                'preview': request.build_absolute_uri(story.content.url),
                'link': '',
                'linkText': '',
                'time': created_timestamp
            })
        
        stories_list.append({
            'id': str(user.id),
            'photo': user.profile.avatar,
            'name': user.username,
            'link': '',
            'lastUpdated': int(data['stories'][0].created_at.timestamp() * 1000),
            'items': items
        })
    
    # Convert to JSON
    try:
        stories_json = json.dumps(stories_list, cls=DjangoJSONEncoder)
        print(f"Sending {len(stories_list)} users' stories to template")
    except Exception as e:
        print(f"Error serializing stories: {e}")
        stories_json = '[]'
    context = {
        'post_items' : post_items,
        'stories' : stories_json,
        'suggested_users' : suggested_users
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

def PostEdit(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    form = PostEditForm(instance = post)

    if request.method == "POST":
        form = PostEditForm(request.POST,instance=post)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {
        'post' : post,
        'form' : form
    }
    return render(request,'post/post-edit.html',context)

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
    
def PostDelete(request,post_id):
    post = get_object_or_404(Post,id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect('home')
    
    return render(request,'post/post-delete.html',{'post':post})

def Tags(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    posts = Post.objects.filter(tag=tag).order_by('-posted')

    context={
        'posts' : posts,
        'tag' : tag
    }   
    return render(request,'post/tag.html',context)

def like_toggle(model):
    def inner_func(func):
        def wrapper(request,*args,**kwargs):
            post = get_object_or_404(model,id=kwargs.get('post_id'))
            user_exist = post.likes.filter(id=request.user.id).exists()

            if user_exist:
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True
                
            return func(request,post,liked)
        return wrapper
    return inner_func

@like_toggle(Post)
def like_post(request, post, liked):
    if liked and request.user != post.user:
        notify.send(
            request.user,
            recipient=post.user,
            verb="liked your post",
            target=post
        )
    return render(request, 'snippets/like_count.html', {'post': post})

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
        

def PostReport(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.parent_post = post
            report.save()
            # Redirect to the same post detail page after saving the comment
            return redirect('home') 

    else:
        form = PostReportForm()  # Initialize an empty form for GET requests

   
    context = {
        'post': post,
        'form': form,  # Use the correct variable name for comments
    }

    return render(request, 'post/post-report.html', context)
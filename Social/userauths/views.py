from django.shortcuts import render,get_object_or_404
from django.urls import resolve
from django.core.paginator import Paginator

from .models import Profile
from django.contrib.auth.models import User
from post.models import Post,Follow,Stream

def UserProfile(request, username):
    # Ensure the profile exists
    Profile.objects.get_or_create(user=request.user)
    
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    
    url_name = resolve(request.path).url_name
    
    if url_name == 'profile':
        # Get the user's posts
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        # Get the user's favourite posts
        posts = profile.favourite.all()
    
    #Tracking Profile Stats
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)
    
    context = {
        'posts_paginator': posts_paginator,
        'posts' : posts,
        'profile': profile,
        'post_count' : post_count,
        'following_count' : following_count,
        'followers_count' : followers_count,
    }
    
    return render(request, "userauths/profile.html", context)
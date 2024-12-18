from django.shortcuts import render,redirect,get_object_or_404
from django.urls import resolve,reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db import transaction

from .models import Profile
from django.contrib.auth.models import User
from post.models import Post,Follow,Stream
from .forms import EditProfileForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def UserProfile(request, username=None):
    # If username is None, it’s the logged-in user's profile
    if username is None or username == request.user.username:
        user = request.user
        profile = Profile.objects.get(user=user)
        
        # Determine if we're showing saved posts or user's posts
        url_name = resolve(request.path).url_name
        if url_name == 'profile':
            posts = Post.objects.filter(user=user).order_by('-posted')
        else:
            posts = profile.favourite.all()
    else:
        # Viewing another user's profile
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(user=user).order_by('-posted')
    
    # Profile stats
    post_count = posts.count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts_paginator': posts_paginator,
        'posts': posts,
        'profile': profile,
        'post_count': post_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'follow_status': follow_status,
    }

    return render(request, "userauths/profile.html", context)

@login_required
def follow(request,username,option):
    user = request.user
    following = get_object_or_404(User,username=username)

    f,created = Follow.objects.get_or_create(following=following,follower=request.user)

    if int(option) == 0:
        f.delete()
        Stream.objects.filter(following=following, user=request.user).all().delete()
    else:
        posts = Post.objects.filter(user=following)[:25]
        with transaction.atomic():
            for post in posts:
                Stream.objects.create(post=post,user=request.user,date=post.posted,following=following)
        
    return HttpResponseRedirect(reverse('userprofile',args=[username]))

@login_required
def EditProfile(request):
    form = EditProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = EditProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print("Form errors:", form.errors)

    if request.path == reverse('profile-onboarding'):
        template = 'userauths/profile_onboarding.html'
    else:
        template = 'userauths/editprofile.html'
    return render(request,template,{'form' : form})

@login_required
def DeleteProfile(request):
    user = request.user

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request,'Account deleted, Hope to see you again')
        return redirect('home')
    return render(request,'userauths/deleteprofile.html')
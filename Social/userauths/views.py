from django.shortcuts import render,redirect,get_object_or_404
from django.urls import resolve,reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db import transaction

from .models import Profile
from django.contrib.auth.models import User
from post.models import Post,Follow,Stream
from .forms import EditProfileForm

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
    follow_status = Follow.objects.filter(following=user,follower=request.user).exists()
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
        'follow_status' : follow_status,
    }
    
    return render(request, "userauths/profile.html", context)

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
        
    return HttpResponseRedirect(reverse('profile',args=[username]))

def EditProfile(request):
    form = EditProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = EditProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile',request.user.username)
        else:
            print("Form errors:", form.errors)
    return render(request,'userauths/editprofile.html',{'form' : form})
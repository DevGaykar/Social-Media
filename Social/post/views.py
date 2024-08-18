from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import  login_required
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse

from post.models import Tag,Stream,Follow,Post,Likes
from django.contrib.auth.models import User
from post.forms import NewPostForm



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
    context ={
        'post':post
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

def like(request,post_id):
    user = request.user
    post=Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user,post=post)

    if not liked.exists():
        Likes.objects.create(user=user,post=post)
        current_likes += 1
        
    else:
        liked.delete()
        current_likes =  current_likes - 1
       
    post.likes =  current_likes
    post.save()


    return HttpResponseRedirect(reverse('post-details',args=[post_id]))

  
from datetime import timedelta
from django.utils import timezone
import json
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from story.models import Story
from post.models import Follow
from django.http import JsonResponse

@login_required
def add_story(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
        
    try:
        story_content = request.FILES.get('content')
        if not story_content:
            return JsonResponse({'success': False, 'message': 'No content uploaded'})
            
        content_type = story_content.content_type.split('/')[0]
        if content_type not in ['image', 'video']:
            return JsonResponse({'success': False, 'message': 'Invalid file type'})
            
        story = Story.objects.create(
            user=request.user,
            content=story_content,
            created_at=timezone.now(),
            expires_at=timezone.now() + timedelta(hours=24)
        )
        
        return JsonResponse({'success': True, 'message': 'Story added successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# @login_required    
# def stories(request):
#     stories_list = []
#     print("\n=== Processing stories ===")

#      # Get user's own stories
#     user_stories = Story.objects.filter(
#         user=request.user,
#         expires_at__gt=timezone.now()
#     ).order_by('-created_at')
    
#     if user_stories.exists():
#         items = []
#         for story in user_stories:
#             items.append({
#                 'id': str(story.id),
#                 'type': story.content_type(),
#                 'length': 3,
#                 'src': request.build_absolute_uri(story.content.url),
#                 'preview': request.build_absolute_uri(story.content.url),
#                 'link': '',
#                 'linkText': '',
#                 'time': int(story.created_at.timestamp() * 1000),
#                 'canDelete': True,  
#             })
            
#         stories_list.append({
#             'id': str(request.user.id),
#             'photo': request.user.profile.avatar,
#             'name' : 'Your Story',
#             'link': '',
#             'lastUpdated': int(user_stories.first().created_at.timestamp() * 1000),
#             'items': items
#         })
    
#     # Get all active stories from followed users in a single query
#     active_stories = Story.objects.select_related('user', 'user__profile').filter(
#         user__in=Follow.objects.filter(follower=request.user).values_list('following', flat=True), 
#         expires_at__gt=timezone.now()
#     ).order_by('user', '-created_at')
    
#     # Group stories by user
#     user_stories = {}
#     for story in active_stories:
#         if story.user_id not in user_stories:
#             user_stories[story.user_id] = {
#                 'user': story.user,
#                 'stories': []
#             }
#         user_stories[story.user_id]['stories'].append(story)
    
#     # Format the stories data
#     for user_id, data in user_stories.items():
#         user = data['user']
#         items = []
        
#         for story in data['stories']:
#             created_timestamp = int(story.created_at.timestamp() * 1000)

#             items.append({
#                 'id': str(story.id),
#                 'type': story.content_type(),
#                 'length': 3,
#                 'src': request.build_absolute_uri(story.content.url),
#                 'preview': request.build_absolute_uri(story.content.url),
#                 'link': '',
#                 'linkText': '',
#                 'time': created_timestamp
#             })
        
#         stories_list.append({
#             'id': str(user.id),
#             'photo': user.profile.avatar,
#             'name': user.username,
#             'link': '',
#             'lastUpdated': int(data['stories'][0].created_at.timestamp() * 1000),
#             'items': items
#         })
    
#     # Convert to JSON
#     try:
#         json_data = json.dumps(stories_list, cls=DjangoJSONEncoder)
#         print(f"Sending {len(stories_list)} users' stories to template")
#     except Exception as e:
#         print(f"Error serializing stories: {e}")
#         json_data = '[]'
    
#     return render(request, 'index.html', {
#         'stories': json_data
#     })





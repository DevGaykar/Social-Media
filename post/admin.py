from django.contrib import admin
from .models import Tag,Post,Follow,Stream,LikedPost,ReportPost

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(LikedPost)
admin.site.register(ReportPost)


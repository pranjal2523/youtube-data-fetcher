from django.contrib import admin
from .models import Video, Comment, ChannelData

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'published_at', 'view_count', 'like_count', 'comment_count')
    search_fields = ('title', 'video_id', 'description')
    list_filter = ('published_at',)
    ordering = ('-published_at',)
    date_hierarchy = 'published_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'video_id', 'published_at', 'like_count', 'reply_to')
    search_fields = ('author_name', 'video_id', 'comment_text')
    list_filter = ('published_at',)
    ordering = ('-published_at',)
    date_hierarchy = 'published_at'


@admin.register(ChannelData)
class ChannelDataAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'video_file', 'comment_file', 'created_date', 'updated_date')
    search_fields = ('user_name',)
    ordering = ('-created_date',)
    date_hierarchy = 'created_date'

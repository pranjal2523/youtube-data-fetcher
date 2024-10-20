from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField()
    duration = models.CharField(max_length=20)
    view_count = models.PositiveBigIntegerField(blank=True, null=True)
    like_count = models.PositiveBigIntegerField(blank=True, null=True)
    comment_count = models.PositiveBigIntegerField(blank=True, null=True)
    default_thumbnail = models.URLField(max_length=200, blank=True, null=True)
    medium_thumbnail = models.URLField(max_length=200, blank=True, null=True)
    high_thumbnail = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.video_id})"


class Comment(models.Model):
    video_id = models.CharField(max_length=20)
    comment_id = models.CharField(max_length=50, unique=True)
    comment_text = models.TextField()
    author_name = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    like_count = models.PositiveIntegerField(blank=True, null=True)
    reply_to = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='replies', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"Comment by {self.author_name} on {self.video_id}"
    

class ChannelData(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    video_file = models.FileField(upload_to='videos_data')
    comment_file = models.FileField(upload_to='comments_data')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name


class Token(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()

    def __str__(self):
        return self.access_token

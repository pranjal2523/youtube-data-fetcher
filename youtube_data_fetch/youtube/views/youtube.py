from django.shortcuts import render
import os
from datetime import timedelta
from django.utils import timezone
from ..models import ChannelData
from ..utils import get_channel_id_by_username, get_videos_by_channel_id, get_comments_by_video_id, save_videos_to_excel, export_comments_to_excel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import ChannelDataSerializer
from rest_framework.permissions import AllowAny

def home(request):
    return render(request, 'home.html')


class YouTubeDataAPIView(APIView):
    permission_classes = [AllowAny]

    def fetch_and_save_youtube_data(self, username, max_comments=100):
        # Check if data for the username already exists and is not older than 1 day
        existing_data = ChannelData.objects.filter(user_name=username).first()
        if existing_data and existing_data.updated_date >= timezone.now() - timedelta(days=1):
            return existing_data.video_file.path, existing_data.comment_file.path
        
        # If old data exists, delete the old files and record
        if existing_data:
            if os.path.isfile(existing_data.video_file.path):
                os.remove(existing_data.video_file.path)
            if os.path.isfile(existing_data.comment_file.path):
                os.remove(existing_data.comment_file.path)
            existing_data.delete()

        # Fetch new data
        channel_id = get_channel_id_by_username(username)
        if not channel_id:
            raise ValueError("Channel not found")

        videos = get_videos_by_channel_id(channel_id)
        video_filename = f'videos_data/videos_data_{username}.xlsx'
        save_videos_to_excel(videos, video_filename)

        all_comments = []
        for video in videos:
            if len(all_comments) >= max_comments:
                break
            video_id = video['video_id']
            comments = get_comments_by_video_id(video_id, max_comments=max_comments - len(all_comments))
            all_comments.extend(comments)

        comment_filename = f'comments_data/comments_data_of_{username}.xlsx'
        export_comments_to_excel(all_comments, comment_filename)

        # Save new record in the database
        new_channel_data = ChannelData.objects.create(
            user_name=username,
            video_file=video_filename,
            comment_file=comment_filename
        )

        return new_channel_data.video_file.path, new_channel_data.comment_file.path

    def post(self, request):
        youtube_url = request.data.get('youtube_url')
        max_comments = int(request.data.get('max_comments', 100))

        if not youtube_url:
            return Response({"error": "YouTube URL is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract the username from the URL
        try:
            username = youtube_url.split('/')[-1]
        except IndexError:
            return Response({"error": "Invalid YouTube URL."}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        video_path, comment_path = self.fetch_and_save_youtube_data(username, max_comments)
        # except ValueError as e:
        #     return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        # except Exception as e:
        #     return Response({"error": "An error occurred while processing your request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Retrieve the newly created/updated data
        channel_data = ChannelData.objects.get(user_name=username)
        serializer = ChannelDataSerializer(channel_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

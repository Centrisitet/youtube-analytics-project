import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import isodate


class PlayList():
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):
        self.pl_id = playlist_id
        playlist = self.youtube.playlists().list(
            part="snippet",
            id=playlist_id).execute()
        self.title = playlist['items'][0]['snippet']['title']
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        print(playlist_videos)
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    def show_best_video(self):
        max_likes = 0
        for v_id in self.video_ids:
            video_id = v_id
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            like_count: int = int(video_response['items'][0]['statistics']['likeCount'])

            if like_count > max_likes:
                max_likes = like_count
                best_id = v_id

        return f"https://youtu.be/{best_id}"

    @property
    def total_duration(self):
        full_duration = timedelta(0)
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                   id=','.join(self.video_ids)
                                                   ).execute()
        for video in video_response['items']:
                # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            full_duration += duration
        return full_duration





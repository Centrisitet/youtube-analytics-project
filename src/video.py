import os
from googleapiclient.discovery import build


class Video():
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        self.id = id_video
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=self.id
                                                   ).execute()
            self.video_title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
        except IndexError:
            self.video_title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None

    def __str__(self):
        return f'{self.video_title}'


class PLVideo():
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str, playlist_id: str):
        self.pl_id = playlist_id
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        num = video_ids.index(video_id)
        self.video_id = video_ids[num]
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id
                                                    ).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return f'{self.video_title}'
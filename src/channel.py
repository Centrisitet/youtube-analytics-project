import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        channel_info = json.dumps(channel, indent=2, ensure_ascii=False)
        channel_info = json.loads(channel_info)
        self.title = channel_info['items'][0]['snippet']['title']
        self.description = channel_info['items'][0]['snippet']['description']
        self.video_count = channel_info['items'][0]['statistics']['videoCount']
        self.sub_count = channel_info['items'][0]['statistics']['subscriberCount']
        self.view_count = channel_info['items'][0]['statistics']['viewCount']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'

    def __repr__(self):
        return f'Channel: {self.title}, Description: {self.description}, Video count: {self.video_count}, Sub count: {self.sub_count}, URL: {self.url}'

    @property
    def id(self):
        return f'{self.__channel_id}'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        channel_info = json.dumps(channel, indent=2, ensure_ascii=False)
        channel_info = json.loads(channel_info)
        print(channel_info)

    def to_json(self, name):
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        channel_info = json.dumps(channel, indent=2, ensure_ascii=False)
        if not os.path.exists(name):
            json_file = open(name, 'w', encoding='UTF-8')
            json_file.write(channel_info)

    @classmethod
    def get_service(cls):
        api_key = cls.api_key
        return cls.youtube

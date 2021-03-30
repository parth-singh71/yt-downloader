import os
from pytube import YouTube, Playlist
from utils import create_dir, get_output_number


class VideoDownloader:
    def __init__(self, link, on_progress_callback, on_complete_callback, download_location=None):
        self.link = link
        self.on_progress_callback = on_progress_callback
        self.on_complete_callback = on_complete_callback
        self.video = YouTube(self.link, on_progress_callback=self.on_progress_callback,
                             on_complete_callback=self.on_complete_callback)
        if download_location:
            self.download_location = download_location
        else:
            self.download_location = os.getcwd()

    def get_info(self, video=None):
        if video is None:
            # To print title
            print("Title :", self.video.title)
            # To get number of views
            print("Views :", self.video.views)
            # To get the length of video
            print("Duration :", self.video.length)
            # To get description
            print("Description :", self.video.description)
            # To get ratings
            print("Ratings :", self.video.rating)
            return self.video.title, self.video.views, self.video.length, self.video.description, self.video.rating
        else:
            # To print title
            print("Title :", video.title)
            # To get number of views
            print("Views :", video.views)
            # To get the length of video
            print("Duration :", video.length)
            # To get description
            print("Description :", video.description)
            # To get ratings
            print("Ratings :", video.rating)
            return video.title, video.views, video.length, video.description, video.rating

    def download(self, link=None, outnum=None):
        if link is None:
            self.get_info()
            stream = self.video.streams.get_lowest_resolution()
            create_dir(f"{self.download_location}/videos/")
            stream.download(output_path=f"{self.download_location}/videos/")
        else:
            video = YouTube(link, on_progress_callback=self.on_progress_callback,
                            on_complete_callback=self.on_complete_callback)
            self.get_info(video=video)
            stream = video.streams.get_lowest_resolution()
            stream.download(
                output_path=f"{self.download_location}/playlists/playlist-{outnum}/")


class PlaylistDownloader(VideoDownloader):
    def __init__(self, link, on_progress_callback, on_complete_callback, download_location=None):
        self.link = link
        self.playlist = Playlist(self.link)
        self.on_progress_callback = on_progress_callback
        self.on_complete_callback = on_complete_callback
        if download_location:
            self.download_location = download_location
        else:
            self.download_location = os.getcwd()

    def get_all_playlist_links(self):
        return self.playlist.video_urls

    def get_num_videos(self):
        return len(self.playlist.videos)

    def download(self):
        links = self.playlist.video_urls
        create_dir(f"{self.download_location}/playlists/")
        outnum = get_output_number(f"{self.download_location}/playlists/") + 1
        for link in links:
            super().download(link, outnum)

# importing tkinter for gui
import tkinter as tk
from tkinter.ttk import Progressbar
from downloader import VideoDownloader, PlaylistDownloader


class GUI():
    def __init__(self):
        self.is_playlist = False
        # creating window
        self.window = tk.Tk()
        # getting screen width and height of display
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        # setting tkinter window size
        self.window.geometry("%dx%d" % (self.width // 4, self.height // 3))
        self.window.title('YTDownloader')
        self.label = tk.Label(
            self.window,
            text="Paste a YouTube video link or a Playlist link to download!",
            wraplength=(self.width // 4) - 20
        )
        self.textbox = tk.Text(
            self.window,
            height=5,
            width=50
        )
        self.var1 = tk.IntVar()
        self.playlist_checkbox = tk.Checkbutton(
            self.window,
            text='Playlist',
            variable=self.var1,
            onvalue=1,
            offvalue=0,
            command=self.update_is_playlist
        )
        self.video_info_label = tk.Label(
            self.window,
            text="",
            wraplength=(self.width // 4) - 20
        )
        self.progress = Progressbar(
            self.window,
            orient=tk.HORIZONTAL,
            length=100,
            mode='determinate'
        )
        self.button = tk.Button(
            self.window,
            text='Download',
            width=25,
            command=self.download
        )
        self.completion_label = tk.Label(
            self.window,
            text="",
            wraplength=(self.width // 4) - 20
        )
        self.build()

    def build(self):
        self.label.pack()
        self.textbox.pack()
        self.playlist_checkbox.pack()
        self.progress.pack()
        self.video_info_label.pack()
        self.button.pack()
        self.completion_label.pack()
        self.window.mainloop()

    def on_progress_callback(self, stream, data_chunk, rem_bytes):
        # print(stream.filesize, rem_bytes)
        percent_remaining = int(
            ((stream.filesize - rem_bytes) / stream.filesize) * 100)
        print(percent_remaining)
        self.progress['value'] = percent_remaining
        self.video_info_label['text'] = stream.title
        self.window.update_idletasks()

    def on_complete_callback(self, stream, file_path):
        print(file_path)
        self.completion_label['text'] = f"Downloaded at location: {file_path}"
        self.window.update_idletasks()

    def download(self):
        link = self.textbox.get("1.0", 'end-1c')
        if self.is_playlist:
            downloader = PlaylistDownloader(
                link=link,
                on_progress_callback=self.on_progress_callback,
                on_complete_callback=self.on_complete_callback,
            )
        else:
            downloader = VideoDownloader(
                link=link,
                on_progress_callback=self.on_progress_callback,
                on_complete_callback=self.on_complete_callback,
            )
        downloader.download()

    def update_is_playlist(self):
        val = self.var1.get()
        if val == 0:
            self.is_playlist = False
        else:
            self.is_playlist = True


GUI()

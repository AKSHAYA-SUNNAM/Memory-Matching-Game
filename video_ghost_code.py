import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import imageio

class VideoPlayer(tk.Tk):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.label = Label(self)
        self.label.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.video = imageio.get_reader(self.video_path)
        self.video_meta = self.video.get_meta_data()
        self.delay = int(1000 / self.video_meta['fps'])
        
        self.width = self.video_meta['size'][0]
        self.height = self.video_meta['size'][1]
        
        self.geometry(f"{self.width}x{self.height}")
        self.bind("<Configure>", self.on_resize)
        self.update_frame()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

    def update_frame(self):
        try:
            frame = self.video.get_next_data()
            image = Image.fromarray(frame)
            image = image.resize((self.width, self.height), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            self.label.config(image=image)
            self.label.image = image
        except IndexError:
            self.video.close()
            return
        
        self.after(self.delay, self.update_frame)

if __name__ == "__main__":
    video_path = 'animation.mp4'  # Path to your video file
    app = VideoPlayer(video_path)
    app.title("Tkinter Video Player")
    app.mainloop()
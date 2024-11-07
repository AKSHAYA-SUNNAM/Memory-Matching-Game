##### anime+background in one tkinter window#####
import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import imageio
import os
import random

# Constants for the memory game
ROWS = 4
COLS = 4
IMAGE_SIZE = 150  # Adjusted size for images and buttons
GRID_PADDING = 20  # Padding around the grid
IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory"  # Update with the correct path
MAX_MOVES = 36  # Maximum allowed moves
BACKGROUND_IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory/game_background.png"  # Update with the path to your background image
VIDEO_PATH = 'ghost_video.mp4'  # Path to your video file

class VideoPlayer(tk.Frame):
    def __init__(self, parent, video_path):
        super().__init__(parent)
        self.parent = parent
        self.video_path = video_path
        
        self.label = Label(self)
        self.label.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.video = imageio.get_reader(self.video_path)
        self.video_meta = self.video.get_meta_data()
        self.delay = int(1000 / self.video_meta['fps'])
        
        self.width = self.parent.winfo_screenwidth()
        self.height = self.parent.winfo_screenheight()
        
        self.frames = []
        self.load_frames()
        
        self.play_count = 0
        self.max_plays = 2
        self.frame_index = 0
        
        self.update_frame()

    def load_frames(self):
        # Preload all frames into memory
        try:
            while True:
                frame = self.video.get_next_data()
                self.frames.append(frame)
        except IndexError:
            pass

    def update_frame(self):
        if self.frame_index >= len(self.frames):
            self.play_count += 1
            if self.play_count < self.max_plays:
                self.frame_index = 0
            else:
                self.parent.show_memory_game()
                return

        frame = self.frames[self.frame_index]
        image = Image.fromarray(frame)
        image = image.resize((self.width, self.height), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        self.label.config(image=image)
        self.label.image = image
        
        self.frame_index += 1
        self.after(self.delay, self.update_frame)
class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matching Game")

        # Load the background image
        self.bg_image = Image.open(BACKGROUND_IMAGE_PATH)
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Create a label to hold the background image
        self.background_label = tk.Label(root, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.buttons = []
        self.images = []
        self.back_image = ImageTk.PhotoImage(Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), color="grey"))  # Back image for cards
        self.load_images()
        self.first = None
        self.second = None
        self.matched = set()
        self.moves = 0
        self.create_buttons()

        self.moves_button = tk.Button(root, text=f"Moves: 0/{MAX_MOVES}", font=("Arial", 16), bg="lightgray", state="disabled")
        self.moves_button.place(relx=1, rely=0.5, anchor="e", x=-20, y=0)  # Place the button beside the grid

    def load_images(self):
        # Load and resize images
        for i in range(1, (ROWS * COLS // 2) + 1):
            image_path = os.path.join(IMAGE_PATH, f"image{i}.png")
            image = Image.open(image_path)
            image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
            self.images.append(ImageTk.PhotoImage(image))
        self.images *= 2  # Duplicate the list for pairs
        random.shuffle(self.images)

    def create_buttons(self):
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                btn = tk.Button(self.root, command=lambda r=r, c=c: self.on_button_click(r, c))
                btn.place(x=GRID_PADDING + c * (IMAGE_SIZE + GRID_PADDING // 2), 
                          y=GRID_PADDING + r * (IMAGE_SIZE + GRID_PADDING // 2), 
                          width=IMAGE_SIZE, height=IMAGE_SIZE)
                btn.config(image=self.back_image)
                row.append(btn)
            self.buttons.append(row)

    def on_button_click(self, r, c):
        if (r, c) in self.matched or (self.first and (r, c) == self.first[0]):
            return

        self.moves += 1
        self.update_moves_button()

        if self.moves > MAX_MOVES:
            self.show_result("You lost! You exceeded the maximum number of moves.")
            self.root.quit()
            return

        btn = self.buttons[r][c]
        image_index = r * COLS + c
        btn.config(image=self.images[image_index])

        if not self.first:
            self.first = ((r, c), btn)
        elif not self.second:
            self.second = ((r, c), btn)
            self.root.after(500, self.check_match)

    def check_match(self):
        first_pos, first_btn = self.first
        second_pos, second_btn = self.second

        if self.images[first_pos[0] * COLS + first_pos[1]] == self.images[second_pos[0] * COLS + second_pos[1]]:
            self.matched.add(first_pos)
            self.matched.add(second_pos)
        else:
            first_btn.config(image=self.back_image)
            second_btn.config(image=self.back_image)

        self.first = None
        self.second = None

        if len(self.matched) == ROWS * COLS:
            self.show_result("Congratulations! You've matched all pairs.")
            self.root.quit()

    def update_moves_button(self):
        self.moves_button.config(text=f"Moves: {self.moves}/{MAX_MOVES}")

    def show_result(self, message):
        messagebox.showinfo("Result", message)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Video Player and Memory Game")
        self.state('zoomed')  # Maximize the window on startup
        self.current_frame = None
        self.show_video_player()

    def show_video_player(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = VideoPlayer(self, VIDEO_PATH)
        self.current_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def show_memory_game(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MemoryGame(self)
        self.current_frame.pack(fill=tk.BOTH, expand=tk.YES)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
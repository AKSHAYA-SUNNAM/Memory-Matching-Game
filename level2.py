import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import os
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Constants for the memory game
ROWS = 5
COLS = 5
IMAGE_SIZE = 115
GRID_PADDING = 10
IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory"
MAX_MOVES = 36
BACKGROUND_IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory/game_background.png"

# Sound file paths
CLICK_SOUND_PATH = "C:/Users/sunna/OneDrive/Desktop/memory/cardflipping.wav"
BACKGROUND_MUSIC_PATH = "C:/Users/sunna/OneDrive/Desktop/memory/ghostbackgroundmusic.mp3"
MATCH_SOUND_PATH = "C:/Users/sunna/OneDrive/Desktop/memory/evillaugh.wav"
LOSE_SOUND_PATH = "C:/Users/sunna/OneDrive/Desktop/memory/winsound.mp3"  # Use lose sound instead of win

# Load sounds
def load_sound(file_path):
    try:
        return pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print(f"Error loading sound {file_path}: {e}")
        return None

click_sound = load_sound(CLICK_SOUND_PATH)
match_sound = load_sound(MATCH_SOUND_PATH)
lose_sound = load_sound(LOSE_SOUND_PATH)

# Load and start playing the background music
try:
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.play(-1)  # Loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
except pygame.error as e:
    print(f"Error loading background music {BACKGROUND_MUSIC_PATH}: {e}")

class MemoryGame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.bg_image = Image.open(BACKGROUND_IMAGE_PATH)
        self.bg_image = self.bg_image.resize((self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.pack(fill=tk.BOTH, expand=tk.YES)

        self.buttons = []
        self.images = []
        self.back_image = ImageTk.PhotoImage(Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), color="lightblue"))
        self.load_images()
        self.first = None
        self.second = None
        self.matched = set()
        self.moves = 0
        self.create_buttons()

        self.moves_label = tk.Label(self, text=f"Moves: {self.moves}/{MAX_MOVES}", font=("Arial", 16), bg="lightgray")
        self.moves_label.place(x=self.parent.winfo_screenwidth() - 200, y=20, width=160, height=50)

    def load_images(self):
        # Load and resize images
        for i in range(1, 13):
            image_path = os.path.join(IMAGE_PATH, f"image_{i}.png")
            image = Image.open(image_path)
            image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
            self.images.append(ImageTk.PhotoImage(image))
        self.images *= 2  # Create pairs of images

        # Add the bomb image
        bomb_image_path = os.path.join(IMAGE_PATH, "bomb.png")
        bomb_image = Image.open(bomb_image_path)
        bomb_image = bomb_image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
        self.bomb_image = ImageTk.PhotoImage(bomb_image)
        
        # Append bomb image to the images list
        self.images.append(self.bomb_image)
        random.shuffle(self.images)

    def create_buttons(self):
        grid_width = COLS * IMAGE_SIZE + (COLS - 1) * GRID_PADDING
        grid_height = ROWS * IMAGE_SIZE + (ROWS - 1) * GRID_PADDING

        x_offset = GRID_PADDING  # Left corner
        y_offset = GRID_PADDING  # Move the grid upwards by setting a smaller fixed value

        for r in range(ROWS):
            row = []
            for c in range(COLS):
                btn = tk.Button(self, command=lambda r=r, c=c: self.on_button_click(r, c))
                btn.place(x=x_offset + c * (IMAGE_SIZE + GRID_PADDING), 
                          y=y_offset + r * (IMAGE_SIZE + GRID_PADDING), 
                          width=IMAGE_SIZE, height=IMAGE_SIZE)
                btn.config(image=self.back_image)
                row.append(btn)
            self.buttons.append(row)

    def on_button_click(self, r, c):
        if (r, c) in self.matched or (self.first and (r, c) == self.first[0]):
            return

        if click_sound:
            click_sound.play()

        self.moves += 1
        self.update_moves_label()

        if self.moves > MAX_MOVES:
            self.show_result("You lost! You exceeded the maximum number of moves.")
            self.parent.quit()
            return

        btn = self.buttons[r][c]
        image_index = r * COLS + c
        btn.config(image=self.images[image_index])

        if self.images[image_index] == self.bomb_image:
            if lose_sound:
                lose_sound.play()
            self.show_result("You clicked the bomb! You lost the game.")
            self.parent.quit()
            return

        if not self.first:
            self.first = ((r, c), btn)
        elif not self.second:
            self.second = ((r, c), btn)
            self.after(500, self.check_match)

    def check_match(self):
        first_pos, first_btn = self.first
        second_pos, second_btn = self.second

        if self.images[first_pos[0] * COLS + first_pos[1]] == self.images[second_pos[0] * COLS + second_pos[1]]:
            self.matched.add(first_pos)
            self.matched.add(second_pos)
            if match_sound:
                match_sound.play()
        else:
            first_btn.config(image=self.back_image)
            second_btn.config(image=self.back_image)

        self.first = None
        self.second = None

        if len(self.matched) == ROWS * COLS - 1:  # All pairs matched, excluding the bomb
            self.parent.quit()

        pygame.mixer.music.set_volume(1.0)

    def update_moves_label(self):
        self.moves_label.config(text=f"Moves: {self.moves}/{MAX_MOVES}")

    def show_result(self, message):
        messagebox.showinfo("Result", message)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Game")
        self.state('zoomed')
        self.current_frame = None
        self.show_memory_game()

    def show_memory_game(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MemoryGame(self)
        self.current_frame.pack(fill=tk.BOTH, expand=tk.YES)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

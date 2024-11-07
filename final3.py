import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
from PIL.Image import Resampling
import imageio
import os
import random

# Constants
ROWS = 4
COLS = 4
IMAGE_SIZE = 150  # Adjusted size for images and buttons
GRID_PADDING = 20  # Padding around the grid
IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory"  # Update with the correct path
MAX_MOVES = 36  # Maximum allowed moves
BACKGROUND_IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory/game_background.png"  # Update with the path to your background image
VIDEO_PATH = 'C:/Users/sunna/OneDrive/Desktop/memory/ghost_video.mp4'  # Path to your video file

class Homepage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Memory Matching Game")

        # Load the background image
        self.original_image = Image.open(os.path.join(IMAGE_PATH, "background_memory.png"))  # Make sure this path is correct
        self.background_image = self.original_image.copy()
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create canvas to hold the background image
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas_image = self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Bind the <Configure> event to the resize_background_image function
        self.canvas.bind("<Configure>", self.resize_background_image)

        self.create_widgets()

    def resize_background_image(self, event):
        new_width = event.width
        new_height = event.height
        self.background_image = self.original_image.resize((new_width, new_height), Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas.itemconfig(self.canvas_image, image=self.background_photo)

        # Update widget positions
        self.canvas.coords(self.title_text, new_width // 2, 50)
        self.canvas.coords(self.description_text, new_width // 2, 130)
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")
        self.quit_button.place(relx=0.5, rely=0.5, anchor="center", y=self.start_button.winfo_height() + 20)  # Adjust y-coordinate for 2 cm spacing

    def create_widgets(self):
        # Title Text
        self.title_text = self.canvas.create_text(self.background_image.width // 2, 50, text="Memory Matching Game", font=("Britannic Bold", 50), fill="#000000", anchor="n")

        # Description Text
        self.description_text = self.canvas.create_text(self.background_image.width // 2, 130, text="Match pairs of cards to win the game!", font=("Britannic Bold", 20), fill="#000000", anchor="n")

        # Start Button
        self.start_button = tk.Button(self, text="Start Game", font=("Britannic Bold", 18), command=self.start_game, relief="raised", overrelief="groove", width=10, height=1, bd=4)
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

        # Quit Button
        self.quit_button = tk.Button(self, text="Quit", font=("Britannic Bold", 18), command=self.quit_game, relief="raised", overrelief="groove", width=10, height=1, bd=4)
        self.quit_button.place(relx=0.5, rely=0.5, anchor="center", y=self.start_button.winfo_height() + 20)  # Adjust y-coordinate for 2 cm spacing

    def start_game(self):
        self.pack_forget()  # Hide the homepage
        self.parent.show_theme_selection_page()  # Show the theme selection page

    def quit_game(self):
        self.parent.quit()

class ThemeSelectionPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.main_frame = tk.Frame(self, bg="linen")
        self.main_frame.pack(expand=True, fill='both')  # Use 'both' to fill both directions

      # Add a title label with increased vertical padding
        self.title_label = tk.Label(self.main_frame, text="Select Theme", font=("Britannic Bold", 40), bg="linen")
        self.title_label.pack(pady=(5, 5))  # Increased padding below the title

        # Create a frame to hold the columns
        self.columns_frame = tk.Frame(self.main_frame, bg="linen")
        self.columns_frame.pack(expand=True, fill='both')  # Fill both directions

        # Create three columns for themes
        self.create_theme_column(0, "fruit.jpg")
        self.create_theme_column(1, "Nohara family.jpg")
        self.create_theme_column(2, "Ghost hunt.jpg")

    def create_theme_column(self, column, image_filename):
        # Create a frame for the column
        column_frame = tk.Frame(self.columns_frame, bg="linen", bd=2, relief="flat", highlightthickness=0)
        column_frame.grid(row=1, column=column, padx=10, pady=0.3)  # Adjusted padding for spacing

        # Load and display the theme image
        image_path = os.path.join(IMAGE_PATH, image_filename)
        if os.path.exists(image_path):
            theme_image = Image.open(image_path)
            theme_image = theme_image.resize((400, 560), Resampling.LANCZOS)  # Adjusted size for images
            theme_photo = ImageTk.PhotoImage(theme_image)
            theme_image_label = tk.Label(column_frame, image=theme_photo, bg="linen")
            theme_image_label.image = theme_photo  # Keep a reference to avoid garbage collection
            theme_image_label.pack(pady=10)
        else:
            print(f"Warning: Image at {image_path} not found!")

        # Start Game Button for the theme
        start_button = tk.Button(column_frame, text="Start Game", font=("Helvetica", 14), command=lambda: self.start_game(image_path))
        start_button.pack(pady=7)

    def start_game(self, theme_image):
        self.pack_forget()
        self.parent.show_video_player(theme_image)

class VideoPlayer(tk.Frame):
    def __init__(self, parent, video_path, theme_image):
        super().__init__(parent)
        self.parent = parent
        self.video_path = video_path
        self.theme_image = theme_image
        
        self.label = Label(self)
        self.label.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.video = imageio.get_reader(self.video_path)
        self.video_meta = self.video.get_meta_data()
       
        self.delay = int(1000 / self.video_meta['fps'])
        self.delay = 1
        
        self.width = self.parent.winfo_screenwidth()
        self.height = self.parent.winfo_screenheight()
        
        self.frames = []
        self.load_frames()
        self.play_count = 0
        self.max_plays = 1  # Change max_plays to 1 to play the video only once
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
                # Switch to memory game after video finishes
                self.parent.show_memory_game(self.theme_image)
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
    def __init__(self, root, theme_image):
        self.root = root
        self.root.title("Memory Matching Game")

        # Load the background image
        self.bg_image = Image.open(BACKGROUND_IMAGE_PATH)
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Create a label to hold the background image
        self.background_label = tk.Label(root, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = tk.Frame(root, bg="RoyalBlue4")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.buttons = []
        self.images = []
        self.back_image = ImageTk.PhotoImage(Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), color="#00688B"))  # Back image for cards
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
        self.show_homepage()

    def show_homepage(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Homepage(self)
        self.current_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def show_theme_selection_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ThemeSelectionPage(self)
        self.current_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def show_video_player(self, theme_image):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = VideoPlayer(self, VIDEO_PATH, theme_image)
        self.current_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def show_memory_game(self, theme_image):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MemoryGame(self, theme_image)
        self.current_frame.pack(fill=tk.BOTH, expand=tk.YES)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

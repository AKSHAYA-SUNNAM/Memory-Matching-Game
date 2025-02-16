import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from PIL.Image import Resampling
import imageio
import os
import pygame

class MemoryMatchingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matching Game")

        # Load the background image
        self.original_image = Image.open("background_memory.png")  
        self.background_image = self.original_image.copy()
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create canvas to hold the background image
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas_image = self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Bind the <Configure> event to the resize_background_image function
        self.canvas.bind("<Configure>", self.resize_background_image)

        self.create_widgets()

        pygame.init()
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound("homepage_music.mp3")  
        self.background_music.play(-1)  # Play the music in a loop

    def stop_music(self):
        self.background_music.stop()

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
        self.title_text = self.canvas.create_text(self.background_image.width // 2, 100, text="Memory Matching Game", font=("Britannic Bold", 50), fill="#000000", anchor="n")

        # Description Text
        self.description_text = self.canvas.create_text(self.background_image.width // 2, 200, text="Match pairs of cards to win the game!", font=("Britannic Bold", 30), fill="#000000", anchor="n")

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Game", font=("Britannic Bold", 18), command=self.start_game, relief="raised", overrelief="groove", width=10, height=1, bd=4)
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

        # Quit Button
        self.quit_button = tk.Button(self.root, text="Quit", font=("Britannic Bold", 18), command=self.quit_game, relief="raised", overrelief="groove", width=10, height=1, bd=4)
        self.quit_button.place(relx=0.5, rely=0.5, anchor="center", y=self.start_button.winfo_height() + 20)  # Adjust y-coordinate for 2 cm spacing

    def start_game(self):
        self.canvas.destroy()
        self.start_button.destroy()
        self.quit_button.destroy()
        self.show_video_player()

    def quit_game(self):
        self.root.quit()

    def show_video_player(self):
        video_path = 'grandma.mp4'  # Path to video file
        VideoPlayer(self.root, video_path, self.show_theme_selection_page)

    def show_theme_selection_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ThemeSelectionPage(self.root, self.stop_music).pack(fill=tk.BOTH, expand=tk.YES)

class VideoPlayer(tk.Frame):
    def __init__(self, parent, video_path, next_callback):
        super().__init__(parent)
        self.parent = parent
        self.video_path = video_path
        self.next_callback = next_callback

        self.label = Label(self)
        self.label.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.video = imageio.get_reader(self.video_path)
        self.video_meta = self.video.get_meta_data()
        self.delay = int(1000 / self.video_meta['fps'])
        
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.bind("<Configure>", self.on_resize)
        
        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()

        self.update_frame()

        # Next Button
        self.next_button = tk.Button(self.parent, text="Next", font=("Britannic Bold", 18), command=self.next_page, relief="raised", overrelief="groove", width=10, height=1, bd=4)
        self.next_button.place(relx=0.5, rely=1.0, anchor="s", y=-50)  # Position at bottom center

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

    def next_page(self):
        self.video.close()
        self.next_callback()

class ThemeSelectionPage(tk.Frame):
    def __init__(self, parent, stop_music_callback):
        super().__init__(parent)
        self.parent = parent
        self.stop_music_callback = stop_music_callback
        self.main_frame = tk.Frame(self, bg="SkyBlue4")
        self.main_frame.pack(expand=True, fill='both')

        # Add a title label with increased vertical padding
        self.title_label = tk.Label(self.main_frame, text="Select Theme", font=("Britannic Bold", 40), bg="SkyBlue4")
        self.title_label.pack(pady=(10, 20))

        # Create a frame to hold the columns
        self.columns_frame = tk.Frame(self.main_frame, bg="SkyBlue4")
        self.columns_frame.pack(expand=True, fill='both')

        # Schedule the creation of the theme columns after the window has been fully rendered
        self.after(100, self.create_theme_columns)

    def create_theme_columns(self):
        # Create three columns for themes
        self.create_theme_column(0, "fruit.jpg", "Hansini.py")
        self.create_theme_column(1, "Nohara family.jpg", "Akshitha.py")
        self.create_theme_column(2, "ghost hunt.jpg", "Akshaya.py")

    def create_theme_column(self, column, image_filename, script_name):
        # Create a frame for the column
        column_frame = tk.Frame(self.columns_frame, bg="SkyBlue4", bd=2, relief="flat", highlightthickness=0)
        column_frame.grid(row=1, column=column, padx=20, pady=10, sticky="nsew")

        # Load and display the theme image
        image_path = os.path.join(IMAGE_PATH, image_filename)
        if os.path.exists(image_path):
            # Get current window dimensions
            window_width = self.parent.winfo_width()
            window_height = self.parent.winfo_height()
            
            # Resize image based on current window size
            new_width = int(window_width / 3) - 40
            new_height = int(window_height * 0.75)
            theme_image = Image.open(image_path)
            theme_image = theme_image.resize((new_width, new_height), Resampling.LANCZOS)
            theme_photo = ImageTk.PhotoImage(theme_image)
            theme_image_label = tk.Label(column_frame, image=theme_photo, bg="SkyBlue4")
            theme_image_label.image = theme_photo  # Keep a reference to avoid garbage collection
            theme_image_label.pack(expand=True, fill='both', pady=10)
        else:
            print(f"Warning: Image at {image_path} not found!")

        # Start Game Button for the theme
        start_button = tk.Button(column_frame, text="Start Game", font=("Helvetica", 14), command=lambda: self.start_game(script_name))
        start_button.pack(pady=7)

        self.columns_frame.columnconfigure(column, weight=1)
        self.columns_frame.rowconfigure(1, weight=1)

    def start_game(self, script_name):
        self.stop_music_callback()  # Stop the music before starting the game
        print(f"Executing {script_name}")
        os.system(f'python {script_name}')  # This will execute the corresponding script

if __name__ == "__main__":
    IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory"  # Update with the correct path

    root = tk.Tk()
    game = MemoryMatchingGame(root)
    root.mainloop()

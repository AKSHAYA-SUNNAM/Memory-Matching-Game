import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# Constants
ROWS = 4
COLS = 4
IMAGE_SIZE = 150  # Adjusted size for images and buttons
GRID_PADDING = 20  # Padding around the grid
IMAGE_PATH = "C:/Users/sunna/OneDrive/Desktop/memory"  # Update with the correct path
MAX_MOVES = 30  # Maximum allowed moves

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matching Game")

        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(expand=True, fill='both')

        # Button Frame
        self.button_frame = tk.Frame(self.main_frame, bg="white")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        self.title_label = tk.Label(self.button_frame, text="Memory Matching Game", font=("Raleway Black", 30))
        self.title_label.pack(pady=(0, 20))  # Add padding below the title

        # Start Button
        self.start_button = tk.Button(self.button_frame, text="Start Game", font=("Helvetica", 14), command=self.go_to_theme_selection)
        self.start_button.pack(pady=(0, 10))

        # Instructions Button
        self.instructions_button = tk.Button(self.button_frame, text="Instructions", font=("Helvetica", 14), command=self.show_instructions)
        self.instructions_button.pack(pady=10)

        # Quit Button
        self.quit_button = tk.Button(self.button_frame, text="Quit", font=("Helvetica", 14), command=self.quit_game)
        self.quit_button.pack(pady=10)

    def go_to_theme_selection(self):
        self.main_frame.pack_forget()
        ThemeSelectionPage(self.root)

    def show_instructions(self):
        instructions = (
            "Memory Matching Game Instructions:\n\n"
            "1. Click on a card to flip it over.\n"
            "2. Remember the picture on the card.\n"
            "3. Click on another card to find its match.\n"
            "4. If the cards match, they stay flipped.\n"
            "5. If they don't match, they flip back.\n"
            "6. Match all pairs to win the game!"
        )
        messagebox.showinfo("Instructions", instructions)

    def quit_game(self):
        self.root.quit()

class ThemeSelectionPage:
    def __init__(self, root):
        self.root = root
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(expand=True, fill='both')

        # Button Frame
        self.button_frame = tk.Frame(self.main_frame, bg="white")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        self.title_label = tk.Label(self.button_frame, text="Select Theme", font=("Helvetica", 24))
        self.title_label.pack(pady=(0, 20))  # Add padding below the title

        # Theme Button
        self.theme_button = tk.Button(self.button_frame, text="Select Theme", font=("Helvetica", 14), command=self.select_theme)
        self.theme_button.pack(pady=(0, 10))

        # Instructions Button
        self.instructions_button = tk.Button(self.button_frame, text="Instructions", font=("Helvetica", 14), command=self.show_instructions)
        self.instructions_button.pack(pady=10)

        # Start Game Button
        self.start_button = tk.Button(self.button_frame, text="Start Game", font=("Helvetica", 14), command=self.start_game)
        self.start_button.pack(pady=10)

    def select_theme(self):
        # Logic to select theme
        messagebox.showinfo("Theme", "Theme selection is not implemented yet.")

    def show_instructions(self):
        instructions = (
            "Memory Matching Game Instructions:\n\n"
            "1. Click on a card to flip it over.\n"
            "2. Remember the picture on the card.\n"
            "3. Click on another card to find its match.\n"
            "4. If the cards match, they stay flipped.\n"
            "5. If they don't match, they flip back.\n"
            "6. Match all pairs to win the game!"
        )
        messagebox.showinfo("Instructions", instructions)

    def start_game(self):
        self.main_frame.pack_forget()
        MemoryGame(self.root)

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matching Game")

        # Calculate total width and height of the grid
        total_width = COLS * (IMAGE_SIZE + GRID_PADDING) + GRID_PADDING
        total_height = ROWS * (IMAGE_SIZE + GRID_PADDING) + GRID_PADDING

        # Center the window on the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - total_width) // 2
        y = (screen_height - total_height) // 2
        root.geometry(f"{total_width + 200}x{total_height}+{x}+{y}")  # Increased window width to accommodate the button

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
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
                self.images.append(ImageTk.PhotoImage(image))
            else:
                print(f"Warning: Image at {image_path} not found!")
        self.images *= 2  # Duplicate the list for pairs
        random.shuffle(self.images)

    def create_buttons(self):
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                btn = tk.Button(self.main_frame, command=lambda r=r, c=c: self.on_button_click(r, c))
                btn.grid(row=r, column=c, padx=GRID_PADDING // 2, pady=GRID_PADDING // 2)
                btn.config(width=IMAGE_SIZE, height=IMAGE_SIZE, image=self.back_image, compound="center")
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

if __name__ == "__main__":
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
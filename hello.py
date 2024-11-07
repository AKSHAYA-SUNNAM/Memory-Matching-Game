import tkinter as tk
def say_hello():
    Label.config(text = "Hello,World!")
root = tk.Tk()
root.title("HELLO WORLD GAME")

Label = tk.Label(root , text="")
Label.pack(pady=10)

button = tk.Button(root, text = "Say Hello", command= say_hello) 
button.pack(pady=10)
root.mainloop()  
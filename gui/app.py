import customtkinter as ctk
from PIL import Image, ImageTk
import os

class PihuApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Pihu AI")
        self.root.geometry("500x600")

        # Load images
        self.assets_path = "assets/avatar"

        self.idle_img = self.load_image("idle.png")

        self.label = ctk.CTkLabel(self.root, image=self.idle_img, text="")
        self.label.pack(pady=20)

        self.text_label = ctk.CTkLabel(self.root, text="Pihu AI Ready 😊", font=("Arial", 18))
        self.text_label.pack()

    def load_image(self, name):
        path = os.path.join(self.assets_path, name)
        img = Image.open(path)
        img = img.resize((300, 300))
        return ImageTk.PhotoImage(img)

    def run(self):
        self.root.mainloop()


def start_gui():
    app = PihuApp()
    app.run()
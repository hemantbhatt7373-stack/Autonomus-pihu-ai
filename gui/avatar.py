import customtkinter as ctk
import os
from PIL import Image

class Avatar:

    def __init__(self):

        self.path = "assets/avatar"

        self.idle = self.load("idle.png")
        self.blink = self.load("blink.png")
        self.talk1 = self.load("talk1.png")
        self.talk2 = self.load("talk2.png")

        self.state = "idle"

    def load(self, file):

        img = Image.open(os.path.join(self.path, file))

        return ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(300,300)
        )
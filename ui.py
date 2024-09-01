from resource_path import ResourcePath
import tkinter as tk

class SecureVault(ResourcePath):
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Vault")
        self.root.minsize(width=500, height=700)
        self.root.maxsize(width=500, height=700)

        icon_path = self.lock()
        self.icon = tk.PhotoImage(file=icon_path)
        self.root.iconphoto(True, self.icon)

        self.set_background_image()

    def set_background_image(self):
        bg_image_path = self.background_image()
        self.bg_image = tk.PhotoImage(file=bg_image_path)

        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

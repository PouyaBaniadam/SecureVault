from resource_path import ResourcePath
import tkinter as tk

class SecureVault(ResourcePath):
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Vault")
        self.root.minsize(width=450, height=650)
        self.root.maxsize(width=450, height=650)

        icon_path = self.lock_png()
        self.icon = tk.PhotoImage(file=icon_path)
        self.root.iconphoto(True, self.icon)
        self.root.configure(bg="#000000")

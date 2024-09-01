import os
import sys


class ResourcePath:
    lock_path = None
    background_path = None
    font_path = None

    @classmethod
    def resource_path(cls, file_name):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath("assets")

        full_path = os.path.join(base_path, file_name)

        return full_path

    @classmethod
    def initialize_paths(cls):
        cls.lock_path = cls.resource_path("lock.png")
        cls.background_path = cls.resource_path("background.png")
        cls.font_path = cls.resource_path("ubuntu.ttf")


ResourcePath.initialize_paths()

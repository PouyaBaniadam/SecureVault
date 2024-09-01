import os
import sys


class ResourcePath:
    @classmethod
    def resource_path(cls, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath("assets")
        return os.path.join(base_path, relative_path)

    @classmethod
    def lock(cls):
        return cls.resource_path("lock.png")

    @classmethod
    def background_image(cls):
        return cls.resource_path("background.png")

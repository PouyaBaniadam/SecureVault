import os
import sys

class Assets:
	@classmethod
	def resource_path(cls, file_name):
		try:
			base_path = sys._MEIPASS
		except AttributeError:
			base_path = os.path.abspath("assets")
		return os.path.join(base_path, file_name)

	@classmethod
	def initialize_paths(cls):
		cls.background_png = cls.resource_path("background.png")
		cls.export_png = cls.resource_path("export.png")
		cls.generate_password_png = cls.resource_path("generate_password.png")
		cls.import_png = cls.resource_path("import.png")
		cls.lock_ico = cls.resource_path("lock.ico")
		cls.lock_png = cls.resource_path("lock.png")
		cls.padlock_png = cls.resource_path("padlock.png")
		cls.search_password_png = cls.resource_path("search_password.png")
		cls.ubuntu_ttf = cls.resource_path("ubuntu.ttf")
		cls.verified_png = cls.resource_path("verified.png")

Assets.initialize_paths()

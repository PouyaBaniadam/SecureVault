import os

class AssetsGenerator:
    def __init__(self, folder):
        self.folder = folder
        self.base_content = f"""import os
import sys

class Assets:
\t@classmethod
\tdef resource_path(cls, file_name):
\t\ttry:
\t\t\tbase_path = sys._MEIPASS
\t\texcept AttributeError:
\t\t\tbase_path = os.path.abspath("assets")
\t\treturn os.path.join(base_path, file_name)

\t@classmethod
\tdef initialize_paths(cls):
"""

    def generate_python_file(self, output_file):
        file_names = [f for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f))]

        for file_name in file_names:
            attribute_name = file_name.replace('.', '_')
            self.base_content += f'\t\tcls.{attribute_name} = cls.resource_path("{file_name}")\n'

        self.base_content += """
Assets.initialize_paths()
"""

        with open(output_file, 'w') as f:
            f.write(self.base_content)


assets_generator = AssetsGenerator("assets")
assets_generator.generate_python_file("generator/assets.py")

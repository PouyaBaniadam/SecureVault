from PySide6.QtWidgets import QPushButton


class UIUtilities:
    def __init__(self):
        self.selection_color = None
        self.selection_background_color = None
        self.border_color = None
        self.font_size = None
        self.background_color = None
        self.background_color = None
        self.color = None
        self.font_weight = None
        self.border_radius = None
        self.padding = None
        self.text_align = None

    @staticmethod
    def darken_color(color: str, factor: float) -> str:
        """
        This function takes a color and a number between 0 and 1.
        then it will do some math to darken the color.
        usually used for hovering beauties :)
        """
        if color.startswith("#"):
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            dark_rgb = tuple(max(int(c * factor), 0) for c in rgb)
            return f'#{dark_rgb[0]:02x}{dark_rgb[1]:02x}{dark_rgb[2]:02x}'

        return color

    def load_QPushButtonStyle(self, **kwargs) -> None:
        """
        This function loads everything we need as we define a button that inherit from QPushButton
        So it gets all the available arguments and do the magic :)
        """

        self.background_color = kwargs.get("background_color")
        self.color = kwargs.get("color")
        self.font_weight = kwargs.get("font_weight")
        self.border_radius = kwargs.get("border_radius")
        self.padding = kwargs.get("padding")
        self.text_align = kwargs.get("text_align")


    def load_QLineEditStyle(self, **kwargs) -> None:
        self.background_color = kwargs.get("background_color")
        self.color = kwargs.get("color", "#000000")
        self.font_size = kwargs.get("font_size")
        self.border_color = kwargs.get("border_color", "#dddddd")
        self.border_radius = kwargs.get("border_radius")
        self.padding = kwargs.get("padding")
        self.selection_color = kwargs.get("selection_color")
        self.selection_background_color = kwargs.get("selection_background_color")

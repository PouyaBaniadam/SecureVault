class Utilities:
    def __init__(self):
        pass

    @staticmethod
    def print_test() -> None:
        """
        A simple function that prints TESTING.
        This is used for testing purposes.
        """
        print("TESTING...")


    @staticmethod
    def print_text(text: str) -> None:
        """
        Prints the current text
        Usually used for input texts.
        """
        print(f"Current Text: {text}")
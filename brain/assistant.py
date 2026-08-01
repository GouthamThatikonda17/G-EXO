from config import APP_NAME, VERSION, AUTHOR


class GEXOBrain:

    def __init__(self):
        self.name = APP_NAME
        self.version = VERSION
        self.author = AUTHOR

    def greet(self):
        print("=" * 40)
        print(f"{self.name} v{self.version}")
        print("=" * 40)
        print(f"Developer : {self.author}")
        print("System Ready.")
        print("Hello, I am G-EXO.")
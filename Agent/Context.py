class Context:
    def __init__(self, filepath="Agent/context_data.txt"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        try:
            with open(self.filepath, "r") as f:
                pass
        except FileNotFoundError:
            with open(self.filepath, "w") as f:
                pass

    def add_context(self, text):
        with open(self.filepath, "a") as f:
            f.write(text + "\n")

    def get_context(self):
        try:
            with open(self.filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""
        
    def clear_context(self):
        """
        Clears the conversation context by truncating the context file.
        """
        with open(self.filepath, "w") as f:
            f.truncate(0) # This is redundant, opening the file in write mode already does this, but it is good practice

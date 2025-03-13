import os

class Notes:
    """
    A class to manage notes stored in a text file, with operations to add to and clear notes.
    """

    def __init__(self, filepath="Tools/notes.txt"):
        """
        Initializes the Notes object with a specified filepath.

        Args:
            filepath (str): The path to the notes file. Defaults to "Tools/notes.txt".
        """
        self.filepath = filepath
        self._ensure_file_exists()
        self.display_header = "Notes:\n"
        self.display_body = self.get_notes()
        self.display = self.display_header + self.display_body
        

    def _update_display(self, body):
        self.display_body = body
        self.display = self.display_header + self.display_body

    def _ensure_file_exists(self):
        """
        Ensures that the notes file exists. Creates it if it doesn't.
        """
        try:
            with open(self.filepath, "r") as f:
                pass
        except FileNotFoundError:
            with open(self.filepath, "w") as f:
                pass

    def add_note(self, note: str) -> str:
        """
        Adds a note to the notes file.

        Args:
            note (str): The note to add.

        Returns:
            str: A confirmation message.
        """
        with open(self.filepath, "a") as f:
            f.write(note + "\n")
        self._update_display(self.get_notes())
        return f"Added note: '{note}'"

    def clear_notes(self) -> str:
        """
        Clears all notes from the notes file.

        Returns:
            str: A confirmation message.
        """
        with open(self.filepath, "w") as f:
            f.truncate(0)
        self._update_display(self.get_notes())
        return "Cleared all notes."
    
    def get_notes(self) -> str:
        """
        Gets all notes from the notes file.

        Returns:
            str: all of the notes in the notes file.
        """
        try:
            with open(self.filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "Notes file not found"


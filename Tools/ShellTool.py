import os
import subprocess

class ShellTool:

    def __init__(self):
        self.current_directory = os.getcwd()  # Initialize with current directory
        self.display_header = "Terminal Output:\n"
        self.display_body = "None"
        self.display = self.display_header + self.display_body

    def _update_display(self, body):
        self.display_body = body
        self.dipslay = self.display_header + self.display_body

    def get_current_directory(self):
        """Returns the current working directory."""
        self._update_display(self.current_directory)
        return ""
    
    def run_command(self, command: str):
        """Runs a shell command."""
        
        if (input(f"Agent attempting to run command:\n{command}\nProceed? (y/n):") == "y"):
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.current_directory,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self._update_display(result.stdout)
                return f"{command}\n{result.stdout}"
            except subprocess.CalledProcessError as e:
                return f"Command \"{command}\" failed with error:\n{e.stderr}"
        else:
            return f"User denied running command: \"{command}\""

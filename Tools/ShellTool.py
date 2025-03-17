import os
import subprocess

class ShellTool:

    def __init__(self):
        self.current_directory = os.getcwd() + "/Workspace"  # Initialize with current directory
        self.display = "None"

    def get_current_directory(self):
        """Returns the current working directory."""
        self.display = "Terminal: " + self.current_directory
    
    def run_command(self, command: str):
        """Runs a shell command."""
        
        if (input(f"Agent attempting to run command:\n{command}\nProceed? (y/n):") == "y"):
        # if True:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.current_directory,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.display = "Terminal: \n" + result.stdout
                return f"ran command {command}\n"
            except subprocess.CalledProcessError as e:
                self.display = "Terminal: \n" + e.stderr
                return f"Command \"{command}\" failed with error:\n{e.stderr}"
        else:
            return f"User denied running command: \"{command}\""

import subprocess
import os
from typing import Tuple

class ShellTool:
    def __init__(self):
        self.current_directory = os.getcwd()  # Start in the current working directory
        self.instructions = """
        Think about what you want to do, then use a command.

        INSIDE SHELL MODE:
        (to use commands, wrap them inside of ```tool_block ```

        Available Commands:
        <shell command> - executes a shell command, like 'ls -l' or 'pwd'
        exit - Exits shell mode, lets you access other modes

        Examples:

        ```tool_block
        ls -l
        ```

        ```tool_block
        cd /home/user/documents
        ```

        ```tool_block
        pwd
        ```

        ```tool_block
        exit
        ```
        """

    def call_shell(self, command: str) -> str:
        """
        Executes a shell command in the current directory.

        Args:
            command: The shell command to execute.

        Returns:
            The output of the command as a string, or an error message.
        """
        try:
            print(f"Executing shell command: {command} in directory: {self.current_directory}")
            # Use subprocess to run the command
            if input(f"run: {command}? (y/n)") == "y":
                process = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.current_directory,
                    capture_output=True,
                    text=True,
                    check=True
                )
            else:
                return "Command was blocked by user."
            print(f"Shell command output: {process.stdout}")
            return process.stdout
        except subprocess.CalledProcessError as e:
            error_message = f"Error executing command: {e}\nReturn code: {e.returncode}\nStderr: {e.stderr}"
            print(error_message)
            return error_message
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)
            return error_message

    def change_directory(self, directory: str) -> str:
        """
        Changes the current working directory.

        Args:
            directory: The path to the new directory.

        Returns:
            A success message or an error message.
        """
        try:
            # Handle absolute and relative paths
            if os.path.isabs(directory):
                new_directory = directory
            else:
                new_directory = os.path.join(self.current_directory, directory)

            # Check if the directory exists and is a directory
            if not os.path.exists(new_directory):
                return f"Error: Directory '{new_directory}' does not exist."
            if not os.path.isdir(new_directory):
                return f"Error: '{new_directory}' is not a directory."

            os.chdir(new_directory)
            self.current_directory = os.getcwd()
            return f"Changed directory to: {self.current_directory}"
        except Exception as e:
            return f"Error changing directory: {e}"

    def get_current_directory(self) -> str:
        """
        Returns the current working directory.

        Returns:
            The current working directory as a string.
        """
        return self.current_directory

    def route_command(self, command: str) -> Tuple[str, str]:
        """
        Routes commands to the appropriate method within ShellTool.

        Args:
            command: The command string from the agent.

        Returns:
            A Tuple with the context message and the display message
        """
        parts = command.split(" ", 1)
        cmd = parts[0].strip()
        arg = parts[1].strip() if len(parts) > 1 else None
        
        if cmd == "cd":
            if arg is None:
                return [f"Error: No directory provided for 'cd'.", ""]
            result = self.change_directory(arg)
            return [f"Changed directory using shell mode", result]
        elif cmd == "pwd":
            current_dir = self.get_current_directory()
            return ["Checked current directory using shell mode", f"Current Directory: {current_dir}"]
        else:
            result = self.call_shell(command)
            return [f"Executed shell command: {command}", f"OUTPUT:\n{result}"]

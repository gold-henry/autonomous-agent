import asyncio
import os
import pathlib
from Tools.ShellTool import ShellTool
from Tools.Checklist import Checklist
from Tools.Notes import Notes
from Tools.BrowserAgent import BrowserAgent

class tools:
    def __init__(self):
        self.instructions = """
Commands:

Shell Commands:
    shell <linux command> - runs any linux shell command
    shell get_dir - gets the current directory

Most of your work can be completed with linux commands.
Remember to include "shell" before the command, or else the command will not be found.

IMPORTANT: Current directory will always revert. Avoid using cd, and instead use relative paths.

Note Commands:
    note add <note> - adds to notes
    note remove <note> - removes from notes

Whenever you find relevent information, take notes.

Other Commands:
    none - does nothing
    msg <message> - sends message to the user

Messages provide the user with an option to provide new input.
ALWAYS end a task with a message.

Only use one command at a time.

IMPORTANT: Take notes on all relevent content, anything you will have to remember to complete a task.

Remember to use "shell" before your command

PUT COMMANDS INSIDE THE command FIELD!
"""
        self.shell = ShellTool()
        self.notes = ""
        self.display = ""
        self._update_display()
        return
    
    def _update_display(self):
        self.display = f"{self.shell.display}\nDirectory: {self.display_directory_hierarchy()}\n"
        return
    
    def display_directory_hierarchy(self):
        """
        Displays the directory hierarchy of a given directory (defaulting to the current directory).

        Args:
            directory (str): The path to the directory to display. Defaults to ".".
        Returns:
            str: A string representation of the directory hierarchy.
        """
        output = ""
        directory = self.shell.get_current_directory()
        try:
            for root, dirs, files in os.walk(directory):
                level = root.replace(directory, '').count(os.sep)
                indent = ' ' * 4 * level
                output += f"{indent}{os.path.basename(root)}/\n"
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    output += f"{subindent}{f}\n"
            return output
        except FileNotFoundError:
            return f"Error: Directory '{directory}' not found."
        except Exception as e:
            return f"An error occurred: {e}"

    # runs command and updates display
    def run_tools(self, command: str):

        if command.startswith("shell"):
            # Run command
            if command.split("shell ")[1].startswith("get_dir"):
                context = self.shell.get_current_directory()
            else:
                context = self.shell.run_command(command.split("shell ")[1])
            # Update display
            self._update_display()
            # Return context
            return context
        elif command.startswith("note"):
            if command.split("note ")[1].startswith("add"):
                context = self.notes.add_note(command.split("note add ")[1])
            elif command.split("note ")[1].startswith("remove"):
                context = self.notes.clear_notes()
            # Update display
            self._update_display()
            return context
        elif command.startswith("none"):
            return None
        elif command.startswith("msg"):
            return f"Message from CodeAgent: {command.split('msg ')[1]}"
        else:
            # If it is not a known command, just try running it in the terminal (the llm likes dropping "shell" a lot)
            context = self.shell.run_command(command)
            # Update display
            self._update_display()
            return "Tried running command in terminal: " + command + "\n"
    

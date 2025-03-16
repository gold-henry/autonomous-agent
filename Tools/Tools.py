import asyncio
from Tools.SearchWeb import SearchWeb
from Tools.ShellTool import ShellTool
from Tools.Checklist import Checklist
from Tools.Notes import Notes
from Tools.BrowserAgent import BrowserAgent

class tools:
    def __init__(self, broswer_path, api_key):
        self.instructions = """
Commands:


Shell Commands:
    shell <linux command> - runs any linux shell command
    shell get_dir - gets the current directory

Most of your work can be completed with linux commands.
Remember to include "shell" before the command, or else the command will not be found.

Web Commands:
    make_research_agent <prompt> - creates a research agent that can access the web. In <prompt>, give it the information you want to find. All found information goes inside of Notes.

Checklist Commands:
    checklist add <task> - adds a task to the checklist
    checklist check <task_id> - checks an existing task off the checklist
    checklist uncheck <task_id> - unchecks a checked off task
    checklist edit <task_id> <edited_task> - edits an existing task
    checklist remove <task_id> - removes an existing task
    checklist clear - clears the checklist

Use the checklist to keep track of what you have done and what you still need to do.

Note Commands:
    note add <note> - adds to notes
    note remove <note> - removes from notes

Whenever you find relevent information, take notes.

Other Commands:
    none - does nothing
    msg <message> - sends message to the user

Messages provide the user with an option to provide new input.
Always end a task with a message.

Only use one command at a time.

IMPORTANT: Take notes on all relevent content, anything you will have to remember to complete a task.

Remember to use "shell" before your command

PUT COMMANDS INSIDE THE command FIELD!
"""
        self.shell = ShellTool()
        self.browserAgent = BrowserAgent(api_key)
        self.checklist = Checklist()
        self.notes = Notes()
        self.display = f"{self.shell.display}\n{self.checklist.display}\n{self.notes.display}\nBrowser Agent:\n{self.browserAgent.ret}"
        return
    
    def _update_display(self):
        self.display = f"{self.shell.display}\n{self.checklist.display}\n{self.notes.display}\nBrowser Agent:\n{self.browserAgent.ret}"
        return

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
        elif command.startswith("make_research_agent"):
            # Run command
            asyncio.run(self.browserAgent.run_browser_agent(command.split("make_research_agent ")[1]))
            # Return context
            return self.browserAgent.ret
        elif command.startswith("checklist"):
            # Run command
            if command.split("checklist ")[1].startswith("add"):
                context = self.checklist.make_task(command.split("checklist add ")[1])
            elif command.split("checklist ")[1].startswith("check"):
                context = self.checklist.check_off_task(command.split("checklist check ")[1])
            elif command.split("checklist ")[1].startswith("uncheck"):
                context = self.checklist.uncheck_task(command.split("checklist uncheck ")[1])
            elif command.split("checklist ")[1].startswith("edit"):
                parts = command.split(" ")
                task_id = parts[2]
                edited_task = " ".join(parts[3:])
                context = self.checklist.edit_task(task_id, edited_task)
            elif command.split("checklist ")[1].startswith("remove"):
                context = self.checklist.remove_task(command.split("checklist remove ")[1])
            elif command.split("checklist ")[1].startswith("clear"):
                context = self.checklist.clear_checklist()
            # Update display
            self._update_display()
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
            print("Agent: " + command.split("msg ")[1])
            new_prompt = input("User Input: ")
            return f"Sent message to User: {command.split('msg ')[1]}\nUser: {new_prompt}"
        else:
            # If it is not a known command, just try running it in the terminal (the llm likes dropping "shell" a lot)
            context = self.shell.run_command(command)
            # Update display
            self._update_display()
            return "Tried running command in terminal: " + command + "\n"
    

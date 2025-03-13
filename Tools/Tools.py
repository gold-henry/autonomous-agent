from Tools.SearchWeb import SearchWeb
from Tools.ShellTool import ShellTool
from Tools.Checklist import Checklist
from Tools.Notes import Notes

class tools:
    def __init__(self):
        self.instructions = """
Commands:


Shell Commands:
    shell <linux command> - runs any linux shell command
    shell get_dir - gets the current directory

Most of your work can be completed with linux commands.
Remember to include "shell" before the command, or else the command will not be found.

Web Commands:
    web search <query> - performs a google search and displays the links
    web get_search_links - displays the links of the previous search
    web visit <url> - sets the current web page
    web get_page_text - displays the text of the current web page
    web get_page_links - displays the links of the current web page
    web get_page_url - displays the url of the current web page
    web close - closes the current web display

Use the web to look up any information you do not already know. However this tool only works for simple html pages, since it uses curl under the hood.

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
        self.web = SearchWeb()
        self.checklist = Checklist()
        self.notes = Notes()
        self.display = self.shell.display + self.web.display + self.checklist.display + self.notes.display
        return
    
    def _update_display(self):
        self.display = self.shell.display + self.web.display + self.checklist.display + self.notes.display
        return

    # runs command and updates display
    def run_tools(self, command: str):

        if command.startswith("shell"):
            # Run command
            if command.split("shell ")[1].startswith("get_dir"):
                context = self.shell.get_dir()
            else:
                context = self.shell.run_command(command.split("shell ")[1])
            # Update display
            self._update_display()
            # Return context
            return context
        elif command.startswith("web"):
            # Run command
            if command.split("web ")[1].startswith("search"):
                context = self.web.google_search(command.split("web search ")[1])
            if command.split("web ")[1].startswith("visit"):
                context = self.web.visit_url(command.split("web visit ")[1])
            if command.split("web ")[1].startswith("get_search_links"):
                context = self.web.get_search_results_links()
            if command.split("web ")[1].startswith("get_page_links"):
                context = self.web.get_links()
            if command.split("web ")[1].startswith("get_page_text"):
                context = self.web.get_text()
            if command.split("web ")[1].startswith("get_page_url"):
                context = self.web.get_url()
            if command.split("web ")[1].startswith("close"):
                context = self.web.close_display()
            # Update display
            self._update_display()
            # Return context
            return context
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
    

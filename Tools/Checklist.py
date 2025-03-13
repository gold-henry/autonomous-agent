import json
import os
from typing import Tuple, List

class Checklist:
    """
    A class to manage a checklist as a tool, with various operations like adding,
    checking off, getting, editing, removing, and unchecking tasks.
    """

    def __init__(self, filepath="Tools/checklist.json"):
        self.filepath = filepath
        self.tasks = self._load_tasks()
        self.display_header = "Checklist:\n"
        self.display_body = "None"
        self.display = self.display_header + self.display_body

    def _update_display(self, body):
        self.display_body = body
        self.display = self.display_header + self.display_body

    def _load_tasks(self):
        try:
            if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            else:
                 return {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_tasks(self):
        """
        Saves the current tasks to the JSON file.
        """
        with open(self.filepath, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def make_task(self, task):
        task_id = str(len(self.tasks) + 1)
        while task_id in self.tasks:
            task_id = str(int(task_id) + 1)  # Increment until a unique ID is found

        self.tasks[task_id] = {"task": task, "checked": False}
        self._save_tasks()
        # Update Display
        self._update_display(self.display_checklist())
        # Return Context
        return f"made task {task} with id {task_id}"

    def check_off_task(self, id):
        """
        Checks off a task by its ID.

        Args:
            task_id (str): The ID of the task to check off.

        Returns:
            bool: True if the task was successfully checked off, False otherwise.
        """
        if id in self.tasks:
            self.tasks[id]["checked"] = True
            self._save_tasks()
            # Update display
            self._update_display(self.display_checklist())
            return f"checked off: {self.tasks[id]}"
        return f"tried checking off task {id}, but it was not found."

    def uncheck_task(self, id):
        if id in self.tasks:
            self.tasks[id]["checked"] = False
            self._save_tasks()
            # Update display
            self._update_display(self.display_checklist())
            return f"unchecked task {self.tasks[id]}"
        return f"tried unchecking task {id}, but it was not found"
    
    def display_checklist(self) -> str:
        checklist_display = ""
        for task_id, task_data in self.tasks.items():
            checklist_display += (task_data["task"] + " id:" + str(task_id) + " : " + str(task_data["checked"]) + "\n")
        return "Checklist:\n" + checklist_display + "\n"

    def edit_task(self, id, task):
        if id in self.tasks:
            self.tasks[id]["task"] = task
            self._save_tasks()
            # Update display
            self._update_display(self.display_checklist())
            return f"edited task {self.tasks[id]}"
        return f"Failed to edit task {id}, no task found with that id"

    def remove_task(self, id):
        if id in self.tasks:
            del self.tasks[id]
            self._save_tasks()
            # Update display
            self._update_display(self.display_checklist())
            return f"removed task with id {id}"
        return f"Failed to remove task {id}, no task found with that id"

    def clear_checklist(self):
        self.tasks = {}
        self._save_tasks()
        # Update display
        self._update_display(self.display_checklist())
        return "Cleared Checklist"

from typing import Tuple
from Tools.SearchWeb import SearchWeb
from Tools.ShellTool import ShellTool

class tools:
    def __init__(self):
        self.global_instructions = """
Think about what you want to do, then use a command.

Wrap all commands inside ```tool_block ```
        
Available Commands:
SEARCH - Enters search mode, which gives you acces to internet search related commands.
SHELL = Enters shell mode, which gives you access to linux shell commands.
        
Example:
```tool_block
SEARCH
```
"""
        self.tool_instructions = ""
        self.current_instructions = self.global_instructions
        self.current = "root"
        # initialize tools
        self.search = SearchWeb()
        self.shell = ShellTool()
        return
    
    # Returns (context, display)
    def run_tools(self, response: str) -> Tuple[str, str]:
        """
        Runs tools based on the agent's response.

        Args:
            response: The agent's response string.

        Returns:
            A tuple containing (context, display) if a tool command is found and executed,
            otherwise None.
        """

        # Check if a tool block is present
        if "```tool_block" not in response or "```" not in response:
            print("No tool block found in response.")
            return None

        # Extract the command from the tool block
        try:
            command = response.split("```tool_block\n")[-1]
            command = command.split("\n```")[0]
        except Exception as e:
            print(f"Error parsing command, {e}")
            return None
        

        if self.current == "root":
            self.current_instructions = self.global_instructions
            # Route to specific tool commands or use global commands
            if command.startswith("SEARCH"):
                print("using tool: " + command)
                self.current = "search"
                return ["Switched to search mode", ""]
            elif command.startswith("SHELL"):
                print("using tool: " + command)
                self.current = "shell"
                return ["Switched to shell mode", ""]
            else:
                print("Invalid command for root mode.")
                return None
            
        elif self.current == "search":
            if command.startswith("exit"):
                self.current_instructions = self.global_instructions
                self.current = "root"
                return ["", "Switched to root mode"]
            self.current_instructions = self.search.instructions
            return self.search.route_command(command)
        elif self.current == "shell":
            if command.startswith("exit"):
                self.current_instructions = self.global_instructions
                self.current = "root"
                return ["", "Switched to root mode"]
            self.current_instructions = self.shell.instructions
            return self.shell.route_command(command)

        


        return None
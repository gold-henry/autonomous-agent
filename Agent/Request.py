import json
from typing import Optional

class Request:
    """
    Represents a request to be sent to the agent, containing context, display, instructions, and a prompt.
    """

    def __init__(self, context: Optional[str] = None, display: Optional[str] = None, instructions: Optional[str] = None, prompt: Optional[str] = None):
        """
        Initializes a new Request object.

        Args:
            context: The conversation context.
            display: The current display information.
            instructions: The instructions for the agent.
            prompt: The user's prompt.
        """
        self.context = context
        self.display = display
        self.instructions = instructions
        self.prompt = prompt

    def add_context(self, context: str):
        """Adds the provided string to the context of the request

        Args:
            context (str): the text to add to context
        """
        if self.context is None:
            self.context = ""
        self.context += context
        return

    def add_display(self, display: str):
        """Adds the provided string to the display of the request

        Args:
            display (str): the text to add to display
        """
        if self.display is None:
            self.display = ""
        self.display += display
        return

    def add_instructions(self, instructions: str):
        """Adds the provided string to the instructions of the request

        Args:
            instructions (str): the text to add to instructions
        """
        if self.instructions is None:
            self.instructions = ""
        self.instructions += instructions
        return
        

    def add_prompt(self, prompt: str):
        """Adds the provided string to the prompt of the request

        Args:
            prompt (str): the text to add to prompt
        """
        if self.prompt is None:
            self.prompt = ""
        self.prompt += prompt
        return

    def to_json(self) -> str:
        """
        Converts the Request object to a JSON string.

        Returns:
            A JSON string representing the Request.

        Raises:
            ValueError: If any of the required fields (context, display, instructions, prompt) are not populated.
        """
        
        if not self.instructions:
            raise ValueError("Request field 'instructions' is not populated.")

        data = {
            "context": self.context,
            "display": self.display,
            "instructions": self.instructions,
            "prompt": self.prompt,
        }
        return json.dumps(data, indent=1)

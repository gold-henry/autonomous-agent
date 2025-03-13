import json
from typing import Optional, Dict, List, Union

class Response:
    """
    Represents a response from the agent, containing reasoning and a command.
    """

    def __init__(self, reasoning: Optional[str] = None, command: Optional[str] = None):
        """
        Initializes a new Response object.

        Args:
            reasoning: The agent's reasoning.
            command: The command the agent wants to execute.
        """
        self.reasoning = reasoning
        self.command = command

    def from_json(self, json_str: str) -> str | None:
        """
        Parses a JSON string (which can be a dictionary directly or a list containing a dictionary)
        and populates the Response object's fields.

        Args:
            json_str: The JSON string to parse.

        Returns:
            None if the JSON was parsed successfully.
            An error message string if there was an issue parsing the JSON.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format. Please provide a valid JSON string."

        # Handle both list and dictionary input
        if isinstance(data, list):
            # Check if the list contains exactly one element
            if len(data) != 1:
                return f"Error: Expected a JSON list with a single object, but received a list with {len(data)} objects."
            data = data[0]  # Extract the dictionary from the list

        # Check if data is a dictionary
        if not isinstance(data, dict):
            return f"Error: Expected a JSON object (dictionary), but received {type(data).__name__} instead."

        # Check for extra keys
        extra_keys = set(data.keys()) - {"reasoning", "command"}
        if extra_keys:
            return f"Error: Unexpected fields in JSON: {', '.join(extra_keys)}. Only 'reasoning' and 'command' are allowed."

        # Check for missing keys
        missing_keys = {"reasoning", "command"} - set(data.keys())
        if missing_keys:
            return f"Error: Missing required fields in JSON: {', '.join(missing_keys)}. Please include 'reasoning' and 'command'."

        # Check if values are strings
        if not isinstance(data.get("reasoning"), str):
            return f"Error: the reasoning field must be a string."
        if not isinstance(data.get("command"), str):
            return f"Error: the command field must be a string."

        # Populate fields if everything is correct
        self.reasoning = data["reasoning"]
        self.command = data["command"]
        return None
    
    def output_response(self) -> str:
        """
        returns the current response as a string

        Returns:
            str: the response as a string.
        """
        return f"reasoning:{self.reasoning}\ncommand:{self.command}"

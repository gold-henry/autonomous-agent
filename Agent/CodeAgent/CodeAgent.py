import os
from Agent.gemini_api import GeminiAPI
from Agent.Context import Context
from Agent.Request import Request
from Agent.Response import Response
from Agent.CodeAgent.CodeTools import tools
import datetime

INSTRUCTIONS = """
You are an expert coder. Use good coding practices, such as Functional and Object Oriented programming. Stay organized within directories and take lots of notes on the project.

Respond in the following JSON format: { reasoning: \"...\", command: \"...\" }

"reasoning" and "command" should be your ONLY fields. 

Only ONE dictionary should be returned.

A response must follow this format exactly:
[
    {
        "reasoning": "..."
        "command": "..."
    }
]

Only take a single step.
""" + f"The date / time is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

class CodeAgent:
    def __init__(self):
        """
        Initializes the Agent and the Gemini API, and sets up context.
        """
        self.gemini_api = GeminiAPI()
        self.context = Context("Agent/CodeAgent/context.txt")
        self.tools = tools()
        print("Agent initialized.")

    def _update_context(self, user_directive: str, agent_response: str, tool_output: str):
        """
        Updates the conversation context with the latest user directive and agent response.

        Args:
            user_directive: The user's input.
            agent_response: The agent's output.
        """
        if user_directive:
            self.context.add_context(f"Directive: {user_directive}")
        if agent_response:
            self.context.add_context(f"Reasoning: {agent_response}")
        if tool_output:
            self.context.add_context(f"{tool_output}")

    def _get_context_string(self) -> str:
        """
        Formats the conversation context as a single string for the Gemini API.

        Returns:
            A string representation of the context.
        """
        return self.context.get_context()

    def call_agent(self, user_directive: str = "") -> str:
        """
        Processes a given prompt using the Gemini API, considering the conversation context,
        and returns the response.

        Args:
            user_directive: The directive or question for the agent.

        Returns:
            A string containing the agent's response from Gemini.

        Raises:
            RuntimeError: if there are issues with the Gemini API.
        """

        new_context = ""

        while(new_context.startswith("Message") == False):
            request = Request()

            # Combine context and the current directive
            context_str = self._get_context_string()

            request.add_context(context_str)

            request.add_display(self.tools.display)

            request.add_instructions(self.tools.instructions + "\n" + INSTRUCTIONS)
            
            if user_directive != "":
                request.add_prompt(user_directive)


            print(f"Request: {request.to_json()}")

            response = Response()

            try:
                # Try to parse the response
                text_response = self.gemini_api.generate_content(request.to_json())
                print("Response: " + text_response)
                parse_res = response.from_json(text_response)
                # If there was an error parsing, add the error message and retry
                while (parse_res != None):
                    print("response was not formatted correctly: " + parse_res)
                    request.add_prompt(user_directive + parse_res)
                    text_response = self.gemini_api.generate_content(request.to_json())
                    parse_res = response.from_json(text_response)

                # Run Tools, check if we need to update context
                new_context = self.tools.run_tools(response.command)

                # Update the context
                self._update_context(user_directive, response.reasoning, new_context)
            except Exception as e:
                raise RuntimeError(f"Error during Gemini API call: {e}") from e

            # Set prompt to "" after first pass
            user_directive = ""

        # Return the new_context when it is a message
        return new_context

        

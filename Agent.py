import os
from gemini_api import GeminiAPI
from Tools.Tools import tools
from Context import Context

INSTRUCTIONS = "(to use commands, wrap them inside of ```tool_block ``` \n Available Commands: search \"enter search here\""

class Agent:
    def __init__(self):
        """
        Initializes the Agent and the Gemini API, and sets up context.
        """
        print("Agent initialized.")
        self.gemini_api = GeminiAPI()
        self.context = Context()
        self.tools = tools()
        self.current_display = ""

    def _update_context(self, user_directive: str, agent_response: str, tool_output: str):
        """
        Updates the conversation context with the latest user directive and agent response.

        Args:
            user_directive: The user's input.
            agent_response: The agent's output.
        """
        if user_directive:
            self.context.add_context(f"User: {user_directive}")
        if agent_response:
            self.context.add_context(f"Agent: {agent_response}")
        if tool_output:
            self.context.add_context(f"Tools Output: {tool_output}")

    def _get_context_string(self) -> str:
        """
        Formats the conversation context as a single string for the Gemini API.

        Returns:
            A string representation of the context.
        """
        return "\n".join(self.context.get_context()) + "\n"

    def call_agent(self, user_directive: str) -> str:
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
        print(f"Agent received prompt: {user_directive}")

        # Combine context and the current directive
        context_str = self._get_context_string()
        full_prompt = f"{context_str}\n {self.tools.current_instructions}\nCURRENT DISPLAY: {self.current_display}\nUser: {user_directive}\nAgent:"

        try:
            agent_response = self.gemini_api.generate_content(full_prompt)
            print(f"Agent generated response: {agent_response}")

            # Run Tools, check if we need to update context
            tool_output_tuple = self.tools.run_tools(agent_response)

            if tool_output_tuple:
                tool_output_context, tool_output_display = tool_output_tuple
                self.current_display = tool_output_display
            else:
                tool_output_context = ""
                tool_output_display = ""

            # Update the context
            self._update_context(user_directive, agent_response, tool_output_context)

            return f"Agent: {agent_response}\nTools Output:{tool_output_display}"

        except Exception as e:
            raise RuntimeError(f"Error during Gemini API call: {e}") from e

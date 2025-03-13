import sys
from Agent.Agent import Agent
import time
from Agent.gemini_api import GeminiAPI

def main():
    agent = Agent()
    if len(sys.argv) == 2:
        if sys.argv[1] == "-n":
            agent.context.clear_context()
            agent.tools.checklist.clear_checklist()
            agent.tools.notes.clear_notes()


    user_prompt = input("Provide initial prompt: ")

    # Generate a prompt goal and list of actions
    thinking_api = GeminiAPI("gemini-2.0-pro-exp")
    new_prompt = thinking_api.generate(f"Given the users prompt \"{user_prompt}\", brainstorm a list of what needs to be considered and what concrete steps need to be taken in order to achieve this goal. Output a new longer and significantly more detailed prompt. It should be worded like a command.")

    agent.call_agent(new_prompt)
    while(True):
        time.sleep(10)
        agent.call_agent()

    return

if __name__ == '__main__':
    main()
import sys
from Agent import Agent

def main():
    agent = Agent()
    if sys.argv[1] == "-n":
        agent.context.clear_context()

    while(True):
        print("Current Instructions: " + agent.tools.current_instructions)
        print("Current Display: " + agent.current_display)
        directive = input("Enter Directive: ")
        response = agent.call_agent(directive)
        print(agent.context)

    return

if __name__ == '__main__':
    main()
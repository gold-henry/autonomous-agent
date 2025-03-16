from Tools.Tools import tools

tool = tools()

def main():

    while True:
        user_input = input("Command here: ")
        tool.run_tools(user_input)
        print("Display:")
        print(tool.display)
    
    return

if __name__ == '__main__':
    main()
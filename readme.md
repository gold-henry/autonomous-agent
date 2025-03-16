# WinterAI

## Project Description

Super simple early version of a Manus-like agent.

WinterAI can perform tasks generally on your computer.

- **Agent:** Core agent logic (`Agent/Agent.py`) for decision-making and task execution.
- **Tools:** A collection of tools (`Tools/`) for specific actions like web searching (`Tools/SearchWeb.py`), shell commands (`Tools/ShellTool.py`), note-taking (`Tools/Notes.py`), and checklist management (`Tools/Checklist.py`).
- **Gemini API:** Integration with the Gemini API (`Agent/gemini_api.py`).
- **Context Management:** Handling context and requests/responses (`Agent/Context.py').

## Setup Instructions

To set up and run this project, follow these steps:

1. **Rename Secrets File:**
   - Navigate to the `Agent/` directory.
   - Rename `secrets.example.txt` to `secrets.txt`.

   ```bash
   cd Agent
   mv secrets.example.txt secrets.txt
   cd ..
   ```

2. **Add API Keys:**
   - Open the `Agent/secrets.txt` file.
   - Add your Gemini API key.

   ```txt
   # Example secrets.txt
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   ```

3. **Add Browser Path:**
   - Open the `Agent/secrets.txt` file.
   - Add your browser path.

   ```txt
   # Example secrets.txt
   BROWSER_LOCATION=/usr/bin/google-chrome
   ```

   - Common paths include:

   Linux:
   ```bash
   /usr/bin/google-chrome
   ```

   Windows:
   ```bash
   C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
   ```

   MacOS:
   ```bash
   /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
   ```

4. **Install Dependencies:**
   - Use `pip` to install required dependencies with version ranges specified in `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Agent:**
   - To run the autonomous agent, execute the main script (`main.py`).

   ```bash
   python main.py
   ```

   - to execute with a new agent, run with the -n flag

   ```bash
   python main.py -n
   ```

## Project Structure

```
Autonomous Agent/
├── Agent/
│   ├── __init__.py
│   ├── Agent.py
│   ├── context_data.txt
│   ├── Context.py
│   ├── gemini_api.py
│   ├── Request.py
│   ├── Response.py
│   └── secrets.txt         # API Keys and secrets
├── Tools/
│   ├── __init__.py
│   ├── checklist.json
│   ├── Checklist.py
│   ├── Notes.py
│   ├── notes.txt
│   ├── SearchWeb.py
│   ├── ShellTool.py
│   └── Tools.py
├── .gitignore
├── main.py
└── todo.md
```

## Usage

After providing an initial prompt, the prompt will be expanded to include many smaller steps. These steps will then be executed by an agent that is capable of using shell commands on your machine, searching the internet, and taking notes.

PLEASE NOTE: Shell commands are inherently unsafe. The program will prompt you to approve (y/n) every shell command that is attempted.

The Agent can also message you to ask for further input.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from pydantic import SecretStr
import os
from Tools.Notes import Notes
from dotenv import load_dotenv
load_dotenv()

class BrowserAgent:
    def __init__(self, api_key):

        self.noteTool = Notes()

        self.browser = Browser(
            config=BrowserConfig(
                # Specify the path to your Chrome executable
                chrome_instance_path= self._get_browser_location(),
                # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                # For Linux, typically: '/usr/bin/google-chrome'
            )
        )

        self.api_key = api_key

        self.controller = controller = Controller()

        @controller.action('Always note relevant information with this tool.')
        def add_note(note: str) -> str:
            output = self.noteTool.add_note(note)
            return ActionResult(extracted_content=output)

        @controller.action('Ask user for information')
        def ask_human(question: str) -> str:
            answer = input(f'\n{question}\nInput: ')
            return ActionResult(extracted_content=answer)
        
        self.llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(api_key))
        
        self.ret = None

        return

    async def run_browser_agent(self, task) -> (str | None):
        self.agent = Agent(
            task=task,
            llm=self.llm,
            planner_llm=self.llm,
            planner_interval=3,
            browser=self.browser,
            use_vision=True,
            controller=self.controller,
            save_conversation_path="./Tools/browser_logs/conversation.txt",
        )

        self.browser = Browser(
            config=BrowserConfig(
                chrome_instance_path= self._get_browser_location()
            )
        )

        self.controller =  Controller()

        self.llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key))

        history = await self.agent.run()

        await self.browser.close()
        self.ret = history.final_result()
        return self.ret
    
    def _get_browser_location(self):
        try:
            with open("Agent/secrets.txt", "r") as f:
                for line in f:
                    if line.startswith("BROWSER_LOCATION="):
                        api_key = line.split("=", 1)[1].strip()
                        if not api_key:
                            raise ValueError(
                                "BROWSER_LOCATION is empty in secrets.txt"
                            )
                        return api_key
                raise ValueError("BROWSER_LOCATION not found in secrets.txt")
        except FileNotFoundError:
            raise FileNotFoundError(
                "secrets.txt not found in the current directory."
            )
        

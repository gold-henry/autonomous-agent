import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from pydantic import SecretStr
import os
from Tools.Notes import Notes
from dotenv import load_dotenv
load_dotenv()

task="""I'd like a thorough analysis of Tesla stock, including:

Summary: Company overview, key metrics, performance data and investment recommendations
Financial Data: Revenue trends, profit margins, balance sheet and cash flow analysis
Market Sentiment: Analyst ratings, sentiment indicators and news impact
Technical Analysis: Price trends, technical indicators and support/resistance levels
Compare Assets: Market share and financial metrics vs. key competitors
Value Investor: Intrinsic value, growth potential and risk factors
Investment Thesis: SWOT analysis and recommendations for different investor types

Please take notes in a file called notes.txt in the current directory
Please use the linux command tool to create a html/css/js project in the current directory that displays the information you have gathered.

Please search for new web resources if the ones you find do not work.
Continue until the task is finished.
"""

class BrowserAgent:
    def __init__(self, api_key):

        self.noteTool = Notes()

        self.browser = Browser(
            config=BrowserConfig(
                # Specify the path to your Chrome executable
                chrome_instance_path= self._get_browser_location(),  # macOS path
                # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                # For Linux, typically: '/usr/bin/google-chrome'
            )
        )

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
        self.agent = agent = Agent(
            task=task,
            llm=self.llm,
            browser=self.browser,
            use_vision=True,
            controller=self.controller,
            save_conversation_path="./Tools/browser_logs/conversation.txt",
        )
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
        

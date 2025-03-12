from typing import List, Tuple
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re

class SearchWeb:
    def __init__(self):
        self.current_page_url = None
        self.current_page_text = None
        self.current_page_links = None
        self.search_results_links = []
        self.instructions = """s
Think about what you want to do, then use a command.

INSIDE WEB MODE:
(to use commands, wrap them inside of ```tool_block ```

Available Commands:
visit <url> - visits a website at a specific url
get_links - get all url links on the current page:
search <query> - performs a google search
get_search_links - Gets the list of available links from the last search
exit - Exits search mode, lets you access other modes, like SHELL

Examples:

```tool_block
search dogs

Examples:

```tool_block
search dogs
```

```tool_block
visit https://www.google.com/search?q=dogs
```

```tool_block
get_links
```
"""


    def google_search(self, query: str, num_results: int = 5) -> str:
        """
        Performs a Google search and returns a string of the top result URLs.

        Args:
            query: The search query string.
            num_results: The number of top results to fetch.

        Returns:
            A string containing the URLs of the search results.
        """
        try:
            print(f"Searching Google for: {query}")
            search_results = search(query, num_results=num_results)
            self.search_results_links = list(search_results)
            # Return the search results urls
            return "\n".join(self.search_results_links)
        except Exception as e:
            return f"Error during Google search: {e}"

    def get_search_results_links(self) -> str:
        if not self.search_results_links:
            return "Error: No previous search results found."
        return "\n".join(self.search_results_links)

    def visit_url(self, url: str) -> str:
        """
        Visits a URL, downloads its HTML, and extracts plain text and links.

        Args:
            url: The URL to visit.

        Returns:
            A message indicating success or an error message.
        """
        try:
            # Check if the URL is a Google search results page
            parsed_url = urlparse(url)
            if parsed_url.netloc == "www.google.com" and parsed_url.path == "/search":
                print(
                    "Error: Cannot visit or parse Google search results directly. Please use 'search <query>' to get links and then visit from those results."
                )
                return "Error: Cannot visit or parse Google search results directly. Please use 'search <query>' to get links and then visit from those results."

            print(f"Visiting URL: {url}")
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all text
            self.current_page_text = soup.get_text(separator="\n", strip=True)

            # Extract all links from <a> tags
            self.current_page_links = [
                link.get("href") for link in soup.find_all("a") if link.get("href")
            ]

            self.current_page_url = url
            print("Successfully visited and processed URL")
            return f"Successfully visited and processed URL: {url}"

        except requests.exceptions.RequestException as e:
            self.current_page_url = url
            self.current_page_text = f"Error visiting URL: {url} - {e}"
            self.current_page_links = None
            return f"Error visiting URL: {url} - {e}"

        except Exception as e:
            self.current_page_url = url
            self.current_page_text = f"An unexpected error occurred while visiting URL: {url} - {e}"
            self.current_page_links = None
            return f"An unexpected error occurred while visiting URL: {url} - {e}"

    def get_links(self) -> str:
        """
        Returns a string representation of the links on the current page.

        Returns:
            A string containing the links, or an error message if no page has been visited.
        """
        if self.current_page_links is None:
            return "Error: No links found on this page."
        if not self.current_page_links:
            return "No links found on this page"

        return "\n".join(self.current_page_links)

    # Returns Context and Display
    def route_command(self, command: str) -> Tuple[str, str]:
        parts = command.split(" ", 1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        if cmd == "visit":
            msg = self.visit_url(arg)
            if self.current_page_url and self.current_page_text:
                return [
                    f"Visited {self.current_page_url} using search mode.",
                    f"DISPLAY OUTPUT:\n{self.current_page_text}",
                ]
            else:
                return [f"Failed to visit URL: {arg}. {msg}", ""]
        elif cmd == "get_search_links":
            links = self.get_search_results_links()
            return [f"Retrieved the last search result links.", f"Search Links:\n{links}"]
        elif cmd == "get_links":
            links = self.get_links()
            return ["Retrieved links from current page.", f"LINKS:\n{links}"]
        elif cmd == "search":
            if arg:
                search_results = self.google_search(arg)
                return [f"Searched Google for: {arg}", f"Search Results:\n{search_results}"]
            else:
                return ["Error: No search query provided.", ""]
        else:
            return [f"Error: Unknown command '{cmd}' in search mode.", ""]
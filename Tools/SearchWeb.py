from typing import List, Tuple, Dict
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
        self.display_header = "\nWeb Display:\n"
        self.display_body = "None"
        self.display = self.display_header + self.display_body

    def _update_display(self, body):
        self.display_body = body
        self.display = self.display_header + self.display_body
        return

    # Update the display, returns context
    def google_search(self, query: str) -> str:
        try:
            print(f"Searching Google for: {query}")
            search_results = search(query, stop=10)
            self.search_results_links = list(search_results)

            # Update the display
            self._update_display("\n".join(self.search_results_links))

            # Return the message for context
            return f"\n Google Searched {query} and found {len(self.search_results_links)} results:\n"
        except Exception as e:
            return f"Error during Google search: {e}"

    # Update the display, returns context
    def get_search_results_links(self) -> str:
        if not self.search_results_links:
            return "Error: No previous search results found."
        self._update_display("\n".join(self.search_results_links))
        return "Displayed results of search"

    def visit_url(self, url: str) -> str:
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

            self._update_display(f"{self.current_page_url} is the current page. Use get_text command to see the page text. Use get_links command to see the page links.")

            print("Successfully visited and processed URL.")
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

        self._update_display("\n".join(self.current_page_links))

        return f"Displayed page links for {self.current_page_url}"
    
    def get_text(self) -> str:
        if self.current_page_text is None:
            return "Error: No text found on this page."
        if not self.current_page_text:
            return "No text found on this page"

        self._update_display(self.current_page_text)

        return f"Displayed page text for {self.current_page_url}"
    
    def get_url(self) -> str:
        if self.current_page_url is None:
            return "Error: No current url found."
        if not self.current_page_url:
            return "No current url found"

        self._update_display("\n".join(self.current_page_url))

        return f"Displayed the url: {self.current_page_url}"
    
    def close_display(self):
        self._update_display("None")
        return "Closed web display"

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.ai.generativelanguage_v1beta.types import GenerateContentResponse  # Import for the response type
from pydantic import BaseModel, Field
import time
import json


class GeminiAPI:
    def __init__(self, model="gemini-2.0-flash"):
        """
        Initializes the Gemini API.

        Args:
            api_key: The Gemini API key.
        """
        api_key = self._load_api_key()
        genai.configure(api_key=api_key)
        self.available_models = self.list_models()
        self.model_name = model

        if not self.model_name:
            raise RuntimeError("No suitable model found.")

        self.model = genai.GenerativeModel(self.model_name)
        print(f"Using model: {self.model_name}")

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            # HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            #HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            #HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

    def list_models(self):
        """Lists available models."""
        print("Listing available models...")
        models = [m for m in genai.list_models()]
        for m in models:
            print(f"  - {m.name}: {m.display_name} ({m.supported_generation_methods})")
        return models

    def choose_model(self, available_models):
        """
        Chooses the 'gemini-2.0-flash' model if available, then 'gemini-pro',
        otherwise returns the first text model.
        """
        for model in available_models:
            if "gemini-2.0-flash" in model.name.lower():
                return model.name
        print(
            "Warning: 'gemini-2.0-flash' model not found, attempting to use 'gemini-pro'."
        )
        for model in available_models:
            if "gemini-pro" in model.name.lower():
                return model.name

        print(
            "Warning: 'gemini-pro' model not found, attempting to use another text model."
        )
        for model in available_models:
            if "generateContent" in model.supported_generation_methods:
                return model.name
        return ""

    # Normal
    def generate(self, prompt: str) -> str:
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                response = self.model.generate_content(
                    prompt,
                    safety_settings=self.safety_settings,
                )

                # Check for safety issues, raise exception
                if response.prompt_feedback:
                    block_reason = response.prompt_feedback.block_reason
                    if block_reason:
                        raise RuntimeError(
                            f"The prompt was blocked for safety reasons: {block_reason}"
                        )

                return response.text

            except Exception as e:
                if "429 Resource has been exhausted" in str(e):
                    print(
                        f"Resource limit reached. Waiting for 60 seconds before retrying (attempt {retry_count+1}/{max_retries})..."
                    )
                    time.sleep(60)  # Wait for 60 seconds
                    retry_count += 1
                else:
                    raise RuntimeError(f"Error during Gemini API call: {e}") from e

        raise RuntimeError(
            f"Error: Gemini API call failed after multiple retries. Last error: {e}"
        )
        return

    # Generates JSON
    def generate_content(self, prompt: str) -> str:
        """
        Generates content using the chosen Gemini model.

        Args:
            prompt: The input prompt.

        Returns:
            The generated text response as a JSON string.

        Raises:
            RuntimeError: if there are issues with the Gemini API.
        """
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                response = self.model.generate_content(
                    prompt,
                    safety_settings=self.safety_settings,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                    )
                )

                # Check for safety issues, raise exception
                if response.prompt_feedback:
                    block_reason = response.prompt_feedback.block_reason
                    if block_reason:
                        raise RuntimeError(
                            f"The prompt was blocked for safety reasons: {block_reason}"
                        )

                return response.text

            except Exception as e:
                if "429 Resource has been exhausted" in str(e):
                    print(
                        f"Resource limit reached. Waiting for 60 seconds before retrying (attempt {retry_count+1}/{max_retries})..."
                    )
                    time.sleep(60)  # Wait for 60 seconds
                    retry_count += 1
                else:
                    raise RuntimeError(f"Error during Gemini API call: {e}") from e

        raise RuntimeError(
            f"Error: Gemini API call failed after multiple retries. Last error: {e}"
        )

    def _load_api_key(self) -> str:
        """
        Loads the Gemini API key from the secrets.txt file.

        Returns:
            The Gemini API key as a string.

        Raises:
            FileNotFoundError: If secrets.txt is not found.
            ValueError: If the GEMINI_API_KEY is not found or is empty.
        """
        try:
            with open("Agent/secrets.txt", "r") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        if not api_key:
                            raise ValueError(
                                "GEMINI_API_KEY is empty in secrets.txt"
                            )
                        return api_key
                raise ValueError("GEMINI_API_KEY not found in secrets.txt")
        except FileNotFoundError:
            raise FileNotFoundError(
                "secrets.txt not found in the current directory."
            )

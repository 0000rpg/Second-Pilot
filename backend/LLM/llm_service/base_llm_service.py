from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMService(ABC):
    """
    Abstract Base Class for all Language Model Services.
    Implements the Strategy Pattern base interface.
    """
    def __init__(self, api_key: str, model_name: str = "auto"):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    def generate_content(self, prompt: str, context: str = "", mode: str = "fast") -> Dict[str, Any]:
        """
        Generates content based on the prompt and optional context/mode.
        Returns a dictionary containing the generated text and metadata.
        """
        pass

    @abstractmethod
    def check_content(self, prompt: str, content: str) -> Dict[str, Any]:
        """
        Checks the correctness of provided content against a prompt.
        Should return structured feedback (e.g., correct/incorrect status).
        """
        pass

    @abstractmethod
    def correct_content(self, original_prompt: str, incorrect_content: str, instructions: str) -> Dict[str, Any]:
        """
        Corrects the content based on provided instructions and context.
        Returns the fully corrected text.
        """
        pass

    @abstractmethod
    def consult_context(self, prompt: str, additional_instructions: str) -> Dict[str, Any]:
        """
        Provides enhanced response by consulting with advanced instructions (Think Mode).
        """
        pass
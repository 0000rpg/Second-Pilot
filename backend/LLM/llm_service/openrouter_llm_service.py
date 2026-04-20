import os
from typing import Dict, Any
import requests
from .base_llm_service import LLMService

class OpenRouterLLMService(LLMService):
    """
    Concrete implementation of LLMService using OpenRouter API.
    """
    def __init__(self, api_key: str, model_name: str = "auto"):
        super().__init__(api_key, model_name)
        # Assuming the base URL for chat completions is used here
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def _call_llm(self, messages: list, temperature: float = 0.7) -> Dict[str, Any]:
        """Helper function to handle the actual API call."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"OpenRouter API Error: {e}")
            return {"error": str(e)}

    def generate_content(self, prompt: str, context: str = "", mode: str = "fast") -> Dict[str, Any]:
        """Generates content using the chat completion endpoint."""
        # Constructing messages list for the API call
        messages = [
            {"role": "user", "content": f"Prompt: {prompt}"}
        ]
        if context:
             messages.append({"role": "system", "content": f"Context/Instructions: {context}. Use this information to guide your response."})

        # In a real scenario, mode would influence the system prompt or temperature
        print(f"--- Calling OpenRouter for generation (Mode: {mode}) ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}

    def check_content(self, prompt: str, content: str) -> Dict[str, Any]:
        """Checks correctness using a structured prompt."""
        check_prompt = f"You are an expert reviewer. Based on the following instructions: '{prompt}', review this content: '{content}'. Respond ONLY with a JSON object containing 'status' ('correct' or 'incorrect') and 'feedback' (a brief explanation)."
        messages = [{"role": "user", "content": check_prompt}]
        print("--- Calling OpenRouter for checking ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}

    def correct_content(self, original_prompt: str, incorrect_content: str, instructions: str) -> Dict[str, Any]:
        """Corrects content based on detailed instructions."""
        correction_prompt = f"Original Goal: '{original_prompt}'. Incorrect Content Provided: '{incorrect_content}'. You must correct this content strictly following these rules/instructions: '{instructions}'. Return ONLY the fully corrected text."
        messages = [{"role": "user", "content": correction_prompt}]
        print("--- Calling OpenRouter for correction ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}

    def consult_context(self, prompt: str, additional_instructions: str) -> Dict[str, Any]:
        """Consults context for enhanced response (Think Mode)."""
        consult_prompt = f"Advanced Consultation Required. Primary Prompt: '{prompt}'. Additional Instructions/Thinking Guide: '{additional_instructions}'. Please provide a highly detailed and thoughtful answer that incorporates all guidelines."
        messages = [{"role": "user", "content": consult_prompt}]
        print("--- Calling OpenRouter for consultation ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}

# Note: LMStudioLLMService would be implemented similarly in a separate file.
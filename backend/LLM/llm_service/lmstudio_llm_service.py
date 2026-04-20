import os
from typing import Dict, Any
from .base_llm_service import LLMService

class LMStudioLLMService(LLMService):
    """
    Concrete implementation of LLMService using a local LM Studio endpoint.
    Assumes the service is running locally on http://localhost:1234/v1/chat/completions
    """
    def __init__(self, api_key: str = "local", model_name: str = "auto"):
        # For local services, API key might be ignored or set to a placeholder.
        super().__init__(api_key, model_name)
        self.base_url = "http://localhost:1234/v1/chat/completions"

    def _call_llm(self, messages: list, temperature: float = 0.7) -> Dict[str, Any]:
        """Helper function to handle the actual API call to LM Studio."""
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature
        }
        try:
            # Note: Using a different base URL and potentially simpler auth for local setup
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"LM Studio API Error: {e}")
            return {"error": str(e)}

    def generate_content(self, prompt: str, context: str = "", mode: str = "fast") -> Dict[str, Any]:
        """Generates content using the chat completion endpoint."""
        messages = [
            {"role": "user", "content": f"Prompt: {prompt}"}
        ]
        if context:
             messages.append({"role": "system", "content": f"Context/Instructions: {context}. Use this information to guide your response."})

        print(f"--- Calling LM Studio for generation (Mode: {mode}) ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}

    def check_content(self, prompt: str, content: str) -> Dict[str, Any]:
        """Checks correctness using a structured prompt."""
        check_prompt = f"You are an expert reviewer. Based on the following instructions: '{prompt}', review this content: '{content}'. Respond ONLY with a JSON object containing 'status' ('correct' or 'incorrect') and 'feedback' (a brief explanation)."
        messages = [{"role": "user", "content": check_prompt}]
        print("--- Calling LM Studio for checking ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}

    def correct_content(self, original_prompt: str, incorrect_content: str, instructions: str) -> Dict[str, Any]:
        """Corrects content based on detailed instructions."""
        correction_prompt = f"Original Goal: '{original_prompt}'. Incorrect Content Provided: '{incorrect_content}'. You must correct this content strictly following these rules/instructions: '{instructions}'. Return ONLY the fully corrected text."
        messages = [{"role": "user", "content": correction_prompt}]
        print("--- Calling LM Studio for correction ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}

    def consult_context(self, prompt: str, additional_instructions: str) -> Dict[str, Any]:
        """Consults context for enhanced response (Think Mode)."""
        consult_prompt = f"Advanced Consultation Required. Primary Prompt: '{prompt}'. Additional Instructions/Thinking Guide: '{additional_instructions}'. Please provide a highly detailed and thoughtful answer that incorporates all guidelines."
        messages = [{"role": "user", "content": consult_prompt}]
        print("--- Calling LM Studio for consultation ---")
        result = self._call_llm(messages)
        return {"text": result["choices"][0]["message"]["content"], "metadata": result}
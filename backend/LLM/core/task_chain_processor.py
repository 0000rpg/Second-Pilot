import json
from typing import List, Dict, Any
from llm_service.base_llm_service import LLMService
# Assuming we have a mechanism to select and initialize the correct service (e.g., from key_manager)

class TaskChainProcessor:
    """
    Processes a sequence of tasks defined in a chain structure.
    Manages context, mode application, and calls appropriate action handlers.
    """
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def _apply_global_mode(self, prompt: str, mode: str) -> str:
        """Applies global mode instructions (fast, deep, research) to the prompt."""
        if mode == "deep":
            return f"Deep Dive Mode. Please try to immerse yourself deeply in the problem and provide a highly detailed, multi-faceted analysis." + "\n\n" + prompt
        elif mode == "research":
            return f"Research Mode. Approach this task by first outlining a comprehensive plan of action, gathering necessary background information, and then executing the solution step-by-step." + "\n\n" + prompt
        # 'fast' mode uses the original prompt

        return prompt

    def process_chain(self, chain: List[Dict[str, str]], user_id: str, global_mode: str) -> Dict[str, Any]:
        """
        Processes the entire task chain sequentially.
        Returns a dictionary containing the final result and history.
        """
        context_history = []
        final_result = None

        for step in chain:
            prompt = step["prompt"]
            action = step["action"]
            model = step["model"] # Currently unused, but kept for future expansion

            # 1. Apply global mode to the prompt
            processed_prompt = self._apply_global_mode(prompt, global_mode)

            print(f"\n--- Processing Step: {action} ---")
            
            if action == "generate":
                result = self.llm_service.generate_content(processed_prompt, context=context_history[-1]['text'] if context_history else "", mode=global_mode)
                step_output = result["text"]
                print("Generation successful.")

            elif action == "consult":
                # Consult uses the prompt as both primary and additional instructions
                result = self.llm_service.consult_context(processed_prompt, context=context_history[-1]['text'] if context_history else "")
                step_output = result["text"]
                print("Consultation successful.")

            elif action == "check":
                # Check requires the LLM to review a specific piece of content (which should be passed in the prompt or history)
                # For simplicity, we assume the check is against the last generated text.
                if not context_history:
                    step_output = "Error: Cannot perform 'check' without prior output."
                else:
                    last_content = context_history[-1]['text']
                    result = self.llm_service.check_content(processed_prompt, last_content)
                    step_output = result["text"]
                    print("Check successful.")

            elif action == "correct":
                # Correct requires the original prompt and the incorrect content (last history item)
                if not context_history:
                    step_output = "Error: Cannot perform 'correct' without prior output."
                else:
                    incorrect_content = context_history[-1]['text']
                    result = self.llm_service.correct_content(processed_prompt, incorrect_content, context=context_history[-1]['text']) # Using last text as instruction source for correction
                    step_output = result["text"]
                    print("Correction successful.")

            else:
                step_output = f"Unknown action type: {action}"
                print(f"Error: Unknown action type: {action}")


            # Update context history and final result
            context_history.append({"prompt": prompt, "action": action, "text": step_output})
            final_result = step_output

        return {"final_result": final_result, "history": context_history}
import json
from typing import List, Dict, Any
from llm_service.base_llm_service import LLMService
from llm_service.llm_factory import LLMServiceFactory

class TaskChainProcessor:
    def __init__(self, llm_service: LLMService):
        self.default_llm_service = llm_service

    def _apply_global_mode(self, prompt: str, mode: str) -> str:
        if mode == "deep":
            return f"Deep Dive Mode. Please immerse yourself deeply in the problem and provide a highly detailed, multi-faceted analysis.\n\n{prompt}"
        elif mode == "research":
            return f"Research Mode. First outline a comprehensive plan, gather background information, then execute the solution step-by-step.\n\n{prompt}"
        return prompt

    def _get_service_for_step(self, step_model: str, user_id: str) -> LLMService:
        """Если model != 'auto', пытаемся переключить провайдера (расширение)."""
        if step_model == "auto" or step_model == self.default_llm_service.model_name:
            return self.default_llm_service
        # Здесь можно расширить: например, по model определить провайдера (openrouter/gpt-4o -> openrouter, local/gemma -> lmstudio)
        # Пока возвращаем стандартный
        return self.default_llm_service

    def process_chain(self, chain: List[Dict[str, str]], user_id: str, global_mode: str) -> Dict[str, Any]:
        context_history = []
        final_result = None

        for idx, step in enumerate(chain):
            prompt = step["prompt"]
            action = step["action"]
            model = step.get("model", "auto")

            processed_prompt = self._apply_global_mode(prompt, global_mode)
            llm = self._get_service_for_step(model, user_id)

            print(f"\n--- Step {idx+1}: {action} (model: {llm.model_name}) ---")
            step_output = None

            try:
                if action == "generate":
                    context = context_history[-1]['text'] if context_history else ""
                    result = llm.generate_content(processed_prompt, context=context, mode=global_mode)
                    step_output = result["text"]

                elif action == "consult":
                    context = context_history[-1]['text'] if context_history else ""
                    result = llm.consult_context(processed_prompt, additional_instructions=context)
                    step_output = result["text"]

                elif action == "check":
                    if not context_history:
                        raise ValueError("Cannot 'check' without prior output")
                    last_content = context_history[-1]['text']
                    result = llm.check_content(processed_prompt, last_content)
                    step_output = result["text"]

                elif action == "correct":
                    if not context_history:
                        raise ValueError("Cannot 'correct' without prior output")
                    incorrect_content = context_history[-1]['text']
                    instructions = context_history[-1]['text']  # или можно брать из отдельного поля
                    result = llm.correct_content(original_prompt=processed_prompt, incorrect_content=incorrect_content, instructions=instructions)
                    step_output = result["text"]

                else:
                    raise ValueError(f"Unknown action: {action}")

            except Exception as e:
                step_output = f"ERROR in {action}: {str(e)}"
                print(f"Error: {e}")

            context_history.append({"prompt": prompt, "action": action, "text": step_output})
            final_result = step_output

        return {"final_result": final_result, "history": context_history}
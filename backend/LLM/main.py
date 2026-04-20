import json
import json
from keys_manager.key_distributor import KeyProvider
from llm_service.openrouter_llm_service import OpenRouterLLMService
from core.task_chain_processor import TaskChainProcessor
from logger.logger import error # Import the logging function

def main(input_json: str):
    """
    Main entry point for the ChatBot Backend. Processes a task chain request.
    :param input_json: JSON string containing the user's task chain request.
    """
    try:
        # 1. Parse Input JSON first to catch structural errors immediately
        data = json.loads(input_json)
    except json.JSONDecodeError as e:
        error("Failed to parse input JSON.", details=e, show="critical")
        return {"error": f"Invalid JSON format in the input payload: {str(e)}"}

    try:
        # 2. Initialize Key Provider and select LLM Service (Strategy Pattern)
        key_provider = KeyProvider()
        api_key = key_provider.get_key() # Get a non-busy key hash

        # For demonstration, we default to OpenRouter using the retrieved key
        llm_service: LLMService = OpenRouterLLMService(api_key=api_key) 
        
        print("--- Initializing Task Chain Processor ---")
        processor = TaskChainProcessor(llm_service=llm_service)

        # 3. Extract data and validate chain structure
        chain = data.get("chain", [])
        user_id = data.get("user-id")
        global_mode = data.get("mode", "fast") # Default to fast

        if not chain:
            return {"error": "Input JSON must contain a 'chain' list."}

        # 4. Execute the task chain
        result = processor.process_chain(chain, user_id, global_mode)
        
        print("\n=========================================")
        print("✅ Task Chain Processing Complete.")
        print("=========================================")
        return result["final_result"]

    except Exception as e:
        error(f"Failed to process task chain.", details=e, show="critical") # Use the logger here
        return {"error": f"An unexpected error occurred during processing: {str(e)}"}

if __name__ == "__main__":
    # Example usage simulation (replace with actual API endpoint handling)
    example_input = """
{
    "chain": [
        {"prompt": "Тезисно напиши план действий и правил для разработки хорошего ПО.", "action": "generate", "model": "auto"},
        {"prompt": "Кратко напиши особенности игры 'Сапёр'.", "action": "consult", "model": "auto"},
        {"prompt": "Руководствуясь данными правилами напиши 1 HTML файл - игру 'Сапёр'.", "action": "generate/check/correct/consult", "model": "auto"},
        {"prompt": "Проверь правильность работы.", "action": "check", "model": "auto"},
        {"prompt": "Исправь ошибки.", "action": "correct", "model": "auto"}
    ],
    "user-id": "26-hdy73u2gi8",
    "mode": "deep"
}
"""
    final_output = main(example_input)
    print("\nFinal Output:")
    print(json.dumps(final_output, indent=4, ensure_ascii=False))
if __name__ == "__main__":
    # Example usage simulation (replace with actual API endpoint handling)
    example_input = """
{
    "chain": [
        {"prompt": "Тезисно напиши план действий и правил для разработки хорошего ПО.", "action": "generate", "model": "auto"},
        {"prompt": "Кратко напиши особенности игры \"Сапёр\".", "action": "consult", "model": "auto"},
        {"prompt": "Руководствуясь данными правилами напиши 1 HTML файл - игру \"Сапёр\".", "action": "generate/check/correct/consult", "model": "auto"},
        {"prompt": "Проверь правильность работы.", "action": "check", "model": "auto"},
        {"prompt": "Исправь ошибки.", "action": "correct", "model": "auto"}
    ],
    "user-id": "26-hdy73u2gi8",
    "mode": "deep"
}
"""
    final_output = main(example_input)
    print("\nFinal Output:")
    # Use json.dumps to ensure the output is correctly formatted JSON string, fixing the previous error.
    print(json.dumps(final_output, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    # Example usage simulation (replace with actual API endpoint handling)
    example_input = """
{
    "chain": [
        {"prompt": "Тезисно напиши план действий и правил для разработки хорошего ПО.", "action": "generate", "model": "auto"},
        {"prompt": "Кратко напиши особенности игры \"Сапёр\".", "action": "consult", "model": "auto"},
        {"prompt": "Руководствуясь данными правилами напиши 1 HTML файл - игру \"Сапёр\".", "action": "generate/check/correct/consult", "model": "auto"},
        {"prompt": "Проверь правильность работы.", "action": "check", "model": "auto"},
        {"prompt": "Исправь ошибки.", "action": "correct", "model": "auto"}
    ],
    "user-id": "26-hdy73u2gi8",
    "mode": "deep"
}
"""
    final_output = main(example_input)
    print("\nFinal Output:")
    # Use json.dumps to ensure the output is correctly formatted JSON string, fixing the previous error.
    print(json.dumps(final_output, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    # Example usage simulation (replace with actual API endpoint handling)
    example_input = """
{
    "chain": [
        {"prompt": "Тезисно напиши план действий и правил для разработки хорошего ПО.", "action": "generate", "model": "auto"},
        {"prompt": "Кратко напиши особенности игры \"Сапёр\".", "action": "consult", "model": "auto"},
        {"prompt": "Руководствуясь данными правилами напиши 1 HTML файл - игру \"Сапёр\".", "action": "generate/check/correct/consult", "model": "auto"},
        {"prompt": "Проверь правильность работы.", "action": "check", "model": "auto"},
        {"prompt": "Исправь ошибки.", "action": "correct", "model": "auto"}
    ],
    "user-id": "26-hdy73u2gi8",
    "mode": "deep"
}
"""
    final_output = main(example_input)
    print("\nFinal Output:")
    print(json.dumps(final_output, indent=4, ensure_ascii=False))
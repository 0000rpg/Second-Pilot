import json
from keys_manager.key_distributor import KeyProvider
from llm_service.llm_factory import LLMServiceFactory
from core.task_chain_processor import TaskChainProcessor
from logger.logger import error
import os

def process_chain_request(input_json: str, provider: str = None, model_name: str = None) -> dict:
    """
    Основная функция обработки цепочки.
    :param input_json: JSON-строка с запросом.
    :param provider: 'openrouter' или 'lmstudio' (если None, берётся из .env).
    :param model_name: имя модели (если None, берётся из .env).
    """
    try:
        data = json.loads(input_json)
    except json.JSONDecodeError as e:
        error("Failed to parse input JSON.", details=e)
        return {"error": f"Invalid JSON: {str(e)}"}

    try:
        # Выбор провайдера и ключа
        if provider is None:
            provider = os.getenv("LLM_PROVIDER", "openrouter")
        if model_name is None:
            model_name = os.getenv("MODEL_NAME", "auto")

        api_key = None
        if provider == "openrouter":
            key_provider = KeyProvider()
            api_key = key_provider.get_key()  # возвращает hash, который используется как API-ключ
            if api_key == "error":
                raise Exception("Could not obtain an API key from KeyProvider")

        llm_service = LLMServiceFactory.get_service(provider, api_key, model_name)
        processor = TaskChainProcessor(llm_service=llm_service)

        chain = data.get("chain", [])
        user_id = data.get("user-id", "anonymous")
        global_mode = data.get("mode", "fast")

        if not chain:
            return {"error": "Input JSON must contain a non-empty 'chain' list."}

        result = processor.process_chain(chain, user_id, global_mode)
        return {"result": result["final_result"], "history": result["history"]}

    except Exception as e:
        error(f"Processing failed", details=e)
        return {"error": str(e)}

# Точка входа для командной строки (тестирование)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    example_input = """
{
    "chain": [
        {"prompt": "Тезисно напиши план действий и правил для разработки хорошего ПО.", "action": "generate", "model": "auto"},
        {"prompt": "Кратко напиши особенности игры 'Сапёр'.", "action": "consult", "model": "auto"},
        {"prompt": "Руководствуясь данными правилами напиши 1 HTML файл - игру 'Сапёр'.", "action": "generate", "model": "auto"},
        {"prompt": "Проверь правильность работы.", "action": "check", "model": "auto"},
        {"prompt": "Исправь ошибки.", "action": "correct", "model": "auto"}
    ],
    "user-id": "26-hdy73u2gi8",
    "mode": "deep"
}
"""
    output = process_chain_request(example_input)
    print(json.dumps(output, indent=4, ensure_ascii=False))
from typing import Type, Optional
from .base_llm_service import LLMService
from .openrouter_llm_service import OpenRouterLLMService
from .lmstudio_llm_service import LMStudioLLMService

class LLMServiceFactory:
    """
    Factory class implementing the Strategy Pattern for selecting and initializing 
    the correct LLM service provider.
    """
    @staticmethod
    def get_service(provider: str, api_key: Optional[str], model_name: str = "auto") -> LLMService:
        """
        Returns an initialized LLMService instance based on the specified provider.

        Args:
            provider (str): The name of the service provider ('openrouter' or 'lmstudio').
            api_key (Optional[str]): API key required for authentication (e.g., OpenRouter). 
                                     Can be None if using a local/dummy key.
            model_name (str): Name of the model to use.

        Returns:
            LLMService: An initialized instance of the concrete LLM service.

        Raises:
            ValueError: If the provider is not supported or required parameters are missing.
        """
        provider = provider.lower()
        
        if provider == 'openrouter':
            if not api_key:
                raise ValueError("OpenRouter requires a valid API key.")
            return OpenRouterLLMService(api_key=api_key, model_name=model_name)
        
        elif provider == 'lmstudio':
            # LM Studio often doesn't require an external API key in the same way. 
            # We pass a placeholder or None if the constructor allows it.
            return LMStudioLLMService(api_key="local", model_name=model_name)
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}. Must be 'openrouter' or 'lmstudio'.")

# Example usage (for internal testing):
# openrouter_service = LLMServiceFactory.get_service('openrouter', os.environ['OPENROUTER_API_KEY'])
# lmstudio_service = LLMServiceFactory.get_service('lmstudio', None)
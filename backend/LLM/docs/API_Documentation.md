# API Documentation for ChatBot Backend

## 🚀 Overview
This backend service processes complex, multi-step user requests by executing a predefined chain of actions against various Large Language Models (LLMs). It utilizes the Strategy Pattern to abstract LLM interactions, allowing seamless switching between providers like OpenRouter and LM Studio.

## ⚙️ Core Components

### 1. `TaskChainProcessor`
This is the central orchestrator. It takes a structured JSON payload defining the task chain and executes steps sequentially, managing context and applying global modes.

**Input Payload Structure:**
```json
{
    "chain": [
        {"prompt": "Initial prompt for step 1.", "action": "generate", "model": "auto"},
        {"prompt": "Prompt for step 2.", "action": "consult", "model": "auto"}
    ],
    "user-id": "string",
    "mode": "fast/deep/research"
}
```

**Available Actions (`action`):**
*   **`generate`**: Basic text generation.
*   **`check`**: Reviews the last generated content for correctness based on instructions in `prompt`.
*   **`correct`**: Takes explicit instructions to fix previously incorrect content.
*   **`consult`**: Enhances response quality by providing advanced "Think Mode" guidance (contextual advice).

**Global Modes (`mode`):**
*   **`fast`**: No additional instructions are added; uses the prompt directly.
*   **`deep`**: Adds detailed prompts encouraging deep, multi-faceted analysis to every step.
*   **`research`**: Adds a structured plan/problem-solving framework to guide thinking at every step.

### 2. `LLMService` (Strategy Pattern)
This abstract class defines the common interface for all LLM providers.

| Method | Description | Purpose |
| :--- | :--- | :--- |
| `generate_content(prompt, context, mode)` | Generates content based on a prompt and optional history/mode. | Core text generation. |
| `check_content(prompt, content)` | Validates provided `content` against the rules in `prompt`. | Quality assurance step. |
| `correct_content(original_prompt, incorrect_content, instructions)` | Rewrites `incorrect_content` based on detailed `instructions`. | Bug fixing/Refinement step. |
| `consult_context(prompt, additional_instructions)` | Provides highly thoughtful output by incorporating advanced guidance. | Advanced reasoning (Think Mode). |

### 3. LLM Providers
*   **OpenRouterLLMService**: Implements the strategy using the OpenRouter API. Requires a valid provisioning key.
*   **LMStudioLLMService**: Implements the strategy for local, self-hosted models via LM Studio endpoint.

## 🔑 Key Management (`keys_manager`)
The system uses `KeyProvider` to manage and select available LLM keys (OpenRouter/etc.). It handles:
1.  Retrieving a non-busy key hash.
2.  Toggling the key status (busy/not busy).
3.  Deleting disabled or unused keys.

## 💾 File Structure & Modules
*   `llm_service/`: Contains all LLM service implementations and the base abstract class.
*   `core/`: Contains the `TaskChainProcessor`, which is the main business logic unit.
*   `keys_manager/`: Handles API key lifecycle management.
*   `main.py`: The entry point that initializes services and runs the processor.
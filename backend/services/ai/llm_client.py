import requests

from config import (
    AI_PROVIDER,
    AI_TIMEOUT,
    MODEL_NAME,
    OLLAMA_URL,
    AI_TEMPERATURE,
    AI_TOP_P,
    AI_REPEAT_PENALTY,
    AI_MAX_TOKENS,
)


class LLMClient:
    """
    Handles communication with the configured
    Large Language Model (LLM) provider.
    """

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the configured AI model.
        """

        provider = AI_PROVIDER.lower()

        if provider == "ollama":
            return self._generate_ollama(prompt)

        raise ValueError(
            f"Unsupported AI provider: {AI_PROVIDER}"
        )

    def _generate_ollama(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Ollama and return
        the generated response.
        """

        url = f"{OLLAMA_URL}/api/generate"

        payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": 
            {
                "temperature": AI_TEMPERATURE,
                "top_p": AI_TOP_P,
                "repeat_penalty": AI_REPEAT_PENALTY,
                "num_predict": AI_MAX_TOKENS,
            },
}

        try:

            response = requests.post(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json"
                },
                timeout=AI_TIMEOUT,
            )

            response.raise_for_status()

            data = response.json()

            text = data.get(
                "response",
                "",
            ).strip()

            if not text:

                return (
                    "AI returned an empty response."
                )

            return text

        except requests.exceptions.ConnectionError:

            return (
                "Unable to connect to Ollama. "
                "Ensure Ollama is running."
            )

        except requests.exceptions.Timeout:

            return (
                "AI request timed out."
            )

        except requests.exceptions.HTTPError as e:

            try:

                error = response.json().get(
                    "error",
                    str(e),
                )

            except Exception:

                error = str(e)

            return (
                f"Ollama HTTP error: {error}"
            )

        except Exception as e:

            return (
                f"An unexpected error occurred: {str(e)}"
            )
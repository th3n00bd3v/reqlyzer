from models.request import AnalyzedRequest

from services.ai.llm_client import LLMClient
from services.ai.prompt_builder import PromptBuilder


class AIAnalyzer:
    """
    Uses the configured LLM to generate a
    human-friendly explanation for an analyzed
    HTTP request.
    """

    def __init__(self):

        self.client = LLMClient()

        self.prompt_builder = PromptBuilder()

    def analyze(
        self,
        request: AnalyzedRequest,
    ) -> AnalyzedRequest:
        """
        Generate an AI summary for a single request.
        """

        prompt = self.prompt_builder.build_request_prompt(
            request
        )

        summary = self.client.generate(prompt)

        request.ai_summary = summary

        return request
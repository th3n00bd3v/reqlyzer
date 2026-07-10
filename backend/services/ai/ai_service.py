from models.request import AnalyzedRequest

from services.ai.llm_client import LLMClient
from services.ai.prompt_builder import PromptBuilder


class AIService:
    """
    Generates AI-powered explanations
    using the configured LLM.
    """

    def __init__(self):

        self.client = LLMClient()

        self.prompt_builder = PromptBuilder()

    def analyze_request(
        self,
        request: AnalyzedRequest,
    ) -> AnalyzedRequest:
        """
        Generate an AI explanation
        for a single request.
        """

        prompt = self.prompt_builder.build_request_prompt(
            request
        )

        request.ai_summary = self.client.generate(
            prompt
        )

        return request

    def summarize_har(
        self,
        requests: list[AnalyzedRequest],
    ) -> str:
        """
        Generate an executive summary
        for the HAR file.
        """

        prompt = self.prompt_builder.build_har_summary_prompt(
            requests
        )

        return self.client.generate(
            prompt
        )
        
        try:
            request.ai_summary = self.client.generate(prompt)
        except:
            request.ai_summary = "Unable to generate AI summary."
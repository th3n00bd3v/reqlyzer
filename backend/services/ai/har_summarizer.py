from models.request import AnalyzedRequest

from services.ai.llm_client import LLMClient
from services.ai.prompt_builder import PromptBuilder


class HARSummarizer:
    """
    Generates a user-friendly AI summary
    for an entire HAR capture.
    """

    def __init__(self):

        self.client = LLMClient()

        self.prompt_builder = PromptBuilder()

    def summarize(
        self,
        requests: list[AnalyzedRequest],
    ) -> str:
        """
        Generate an executive summary
        for the entire HAR file.
        """

        if not requests:

            return "No requests were found in the HAR file."

        prompt = self.prompt_builder.build_har_summary_prompt(
            requests
        )

        summary = self.client.generate(prompt)

        return summary
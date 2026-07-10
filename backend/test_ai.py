from services.ai.llm_client import LLMClient

client = LLMClient()

response = client.generate(
    "Reply with exactly: Reqlyzer AI test successful."
)

print("\nAI Response:\n")
print(response)
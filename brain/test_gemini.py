from ai.gemini import GeminiProvider

ai = GeminiProvider()

response = ai.generate("Say hello in one sentence.")

print(response)

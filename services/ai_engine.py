import google.generativeai as genai
from google.generativeai.types import GenerationConfig

class AIEngine:
    def __init__(self, api_key: str, tools: list = None):
        genai.configure(api_key=api_key)
        if tools:
            self.model = genai.GenerativeModel("gemini-2.5-flash", tools=tools)
        else:
            self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_text(self, prompt: str, max_output_tokens: int = 2000) -> str:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=GenerationConfig(max_output_tokens=max_output_tokens)
            )
            if response.candidates:
                return response.candidates[0].content.parts[0].text
            return "No content generated."
        except Exception as e:
            return f"Error generating text: {e}"

    def stream_generate_text(self, prompt: str):
        try:
            response = self.model.generate_content(prompt, stream=True)
            buffer = ""
            for chunk in response:
                if hasattr(chunk, "parts") and chunk.parts:
                    part = chunk.parts[0]
                    if hasattr(part, "text") and isinstance(part.text, str):
                        buffer += part.text
                elif hasattr(chunk, "text") and isinstance(chunk.text, str):
                    buffer += chunk.text

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        yield line.strip()

            if buffer.strip():
                yield buffer.strip()

        except Exception as e:
            yield f"Error streaming text: {e}"

    def start_chat(self, history=None):
        if history is None:
            history = []
        return self.model.start_chat(history=history)

from typing import List, Optional
from google import genai
from google.genai.types import GenerateContentConfig, Tool
import json
from utils.func_call.send_whatsapp import send_whatsapp_message
from utils.func_call.get_whatsapp_contact import get_contact_by_name

class AIEngine:
    def __init__(self, api_key: str, tools: Optional[List[Tool]] = None):
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash" # Atau model lain yang Anda inginkan
        self.tools = tools

    async def stream_generate_text(self, prompt: str):
        async for chunk in await self.client.aio.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt,
            config=GenerateContentConfig(
            tools=[
                send_whatsapp_message,
                get_contact_by_name
            ]
        )):
            # print(chunk)
            text = chunk.text or ""
            # print(text)
            yield f"data: {json.dumps({'text': text})}\n\n"
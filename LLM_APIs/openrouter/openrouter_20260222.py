import os
from openai import OpenAI

# OpenRouter - unified gateway for multiple LLM providers
# Docs: https://openrouter.ai/docs
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)
REQUEST_TIMEOUT = 300.0


# -- chat.completions API (text or vision) --
def call_chat_api(model: str, prompt: str, image_b64: str = "", mime: str = "image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_b64:
        content.insert(0, {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_b64}"}})
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        stream=False,
        timeout=REQUEST_TIMEOUT,
    )
    raw = response.choices[0].message.content or "" if response.choices else ""
    usage = {}
    if response.usage:
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    return raw, usage

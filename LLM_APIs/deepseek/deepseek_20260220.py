import os
from openai import OpenAI

# DeepSeek - OpenAI-compatible endpoint
# Docs: https://api-docs.deepseek.com/
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
REQUEST_TIMEOUT = 180.0


# -- chat.completions API --
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

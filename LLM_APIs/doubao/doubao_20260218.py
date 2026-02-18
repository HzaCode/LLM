import os
from openai import OpenAI

# Volcengine Ark - OpenAI-compatible endpoint
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY", "YOUR_DOUBAO_KEY")
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

client = OpenAI(api_key=DOUBAO_API_KEY, base_url=DOUBAO_BASE_URL)
REQUEST_TIMEOUT = 180.0


# -- Option 1: responses API (for seed-series vision models) --
def call_responses_api(model: str, prompt: str, image_b64: str, mime: str = "image/jpeg"):
    response = client.responses.create(
        model=model,
        input=[{
            "role": "user",
            "content": [
                {"type": "input_image", "image_url": f"data:{mime};base64,{image_b64}"},
                {"type": "input_text", "text": prompt},
            ],
        }],
    )
    raw = ""
    for item in response.output:
        if getattr(item, "type", "") == "message":
            for c in item.content:
                if getattr(c, "type", "") == "output_text":
                    raw = c.text or ""
                    break
            if raw:
                break
    usage = {}
    if hasattr(response, "usage") and response.usage:
        usage = {
            "prompt_tokens": getattr(response.usage, "input_tokens", 0),
            "completion_tokens": getattr(response.usage, "output_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0),
        }
    return raw, usage


# -- Option 2: chat.completions API (for 1.5-series vision models) --
def call_chat_api(model: str, prompt: str, image_b64: str, mime: str = "image/jpeg"):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                {"type": "text", "text": prompt},
            ],
        }],
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

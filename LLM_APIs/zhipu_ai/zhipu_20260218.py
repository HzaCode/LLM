import os
from openai import OpenAI

# Zhipu AI - OpenAI-compatible endpoint
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "YOUR_ZHIPU_KEY")
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

client = OpenAI(api_key=ZHIPU_API_KEY, base_url=ZHIPU_BASE_URL)
REQUEST_TIMEOUT = 180.0


# -- chat.completions API (vision: pass image as image_url content block) --
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
        if (
            hasattr(response.usage, "completion_tokens_details")
            and response.usage.completion_tokens_details
            and hasattr(response.usage.completion_tokens_details, "reasoning_tokens")
        ):
            usage["reasoning_tokens"] = response.usage.completion_tokens_details.reasoning_tokens
    return raw, usage

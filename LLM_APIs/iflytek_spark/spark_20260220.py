import os
from openai import OpenAI

# iFlytek Spark - OpenAI-compatible endpoint
# Docs: https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html
# Auth: use APIPassword from console as Bearer token
SPARK_API_PASSWORD = os.getenv("SPARK_API_PASSWORD", "YOUR_SPARK_API_PASSWORD")
SPARK_BASE_URL = "https://spark-api-open.xf-yun.com/v1/"

client = OpenAI(api_key=SPARK_API_PASSWORD, base_url=SPARK_BASE_URL)
REQUEST_TIMEOUT = 180.0


# -- chat.completions API --
def call_chat_api(model: str, prompt: str):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
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

import os
from openai import OpenAI

# Baidu ERNIE (AI Studio) - OpenAI-compatible endpoint
# Docs: https://ai.baidu.com/ai-doc/AISTUDIO/rm344erns
# Note: old OAuth + REST approach is deprecated; use OpenAI SDK now
AI_STUDIO_API_KEY = os.getenv("AI_STUDIO_API_KEY", "YOUR_AI_STUDIO_KEY")
ERNIE_BASE_URL = "https://aistudio.baidu.com/llm/lmapi/v3"

client = OpenAI(api_key=AI_STUDIO_API_KEY, base_url=ERNIE_BASE_URL)
REQUEST_TIMEOUT = 180.0


# -- chat.completions API --
def call_chat_api(model: str, prompt: str, image_b64: str = "", mime: str = "image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_b64:
        # 确保base64字符串编码正确
        try:
            # 清理base64字符串，移除可能的空白字符
            clean_b64 = image_b64.strip().replace('\n', '').replace('\r', '')
            # 验证base64编码
            import base64
            base64.b64decode(clean_b64 + '==')  # 添加填充以避免错误
            content.insert(0, {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{clean_b64}"}})
        except Exception as e:
            print(f"图像编码错误: {e}")
            # 如果图像编码有问题，跳过图像继续处理
            pass
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

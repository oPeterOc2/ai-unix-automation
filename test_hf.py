from huggingface_hub import InferenceClient
import os

# 換成 Qwen 2.5，這是目前免費 API 最穩定的模型
client = InferenceClient(
    "Qwen/Qwen2.5-7B-Instruct",
    token=os.getenv("HF_TOKEN"),
)

try:
    response = client.chat_completion(
        messages=[{"role": "user", "content": "How to fix 'Permission denied' in Unix?"}],
        max_tokens=100
    )
    print("\nAI 回覆內容：")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\n再次失敗詳情: {e}")
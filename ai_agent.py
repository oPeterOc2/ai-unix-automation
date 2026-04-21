import os
import sys
from huggingface_hub import InferenceClient

def get_ai_diagnostic(error_content):
    token = os.getenv("HF_TOKEN")
    if not token:
        return "Error: 找不到 HF_TOKEN 環境變數。"

    try:
        # 統一使用 Qwen/Qwen2.5-7B-Instruct
        client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", token=token)
        
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "你是一位 Unix 專家。請分析錯誤並給出簡短修復建議。"},
                {"role": "user", "content": f"錯誤日誌如下：\n{error_content}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI 診斷異常: {str(e)}"

if __name__ == "__main__":
    raw_input = sys.stdin.read()
    if raw_input.strip():
        print("\n--- AI 診斷報告 ---")
        print(get_ai_diagnostic(raw_input))
        print("-------------------\n")
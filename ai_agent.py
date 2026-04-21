import os
import sys
import requests

# 設定 AI 模型 (Mistral 是一個平衡速度與能力的優質選擇)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

def get_ai_diagnostic(error_content):
    token = os.getenv("HF_TOKEN")
    if not token:
        return "Error: 找不到 HF_TOKEN 環境變數。"

    headers = {"Authorization": f"Bearer {token}"}
    prompt = f"<s>[INST] 你是一位 Unix 系統專家。請分析以下錯誤訊息，並提供：\n1. 簡短的原因解釋\n2. 具體的修復指令\n\n錯誤訊息：\n{error_content} [/INST]</s>"
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 200}}, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result[0]['generated_text'].split("[/INST]</s>")[-1].strip()
    except Exception as e:
        return f"AI 診斷失敗: {str(e)}"

if __name__ == "__main__":
    # 從 stdin 讀取錯誤日誌 (Pipeline 模式)
    raw_input = sys.stdin.read()
    if raw_input.strip():
        print("\n--- AI 診斷報告 ---")
        print(get_ai_diagnostic(raw_input))
        print("-------------------\n")
# [Security Note] 
# 1. 請使用自己的 Hugging Face Token (HF_TOKEN) 執行。
# 2. 嚴禁將 Token 硬編碼於代碼中，請使用環境變數。

import os
import sys
import re
import time
import queue
import threading
from huggingface_hub import InferenceClient

# --- 配置區 ---
# 可透過環境變數切換後端：'HF' (雲端), 'LOCAL' (127.0.0.1), 'INTERNAL' (企業內部 Server)
LLM_BACKEND = os.getenv("LLM_BACKEND", "HF") 
INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://10.x.x.x:11434/v1") 

MAX_ALERTS_PER_HOUR = 5
ALERT_COUNT = 0
LAST_ALERT_TIME = 0
task_queue = queue.Queue()

# --- 新增：維運診斷類別 ---
class UnixDiagnosticAgent:
    """封裝 AI 診斷邏輯與配置"""
    # 外部環境變數失效或格式錯誤時的最終防線 (Default Values)
    DEFAULT_MAX_TOKENS = 250

    def __init__(self):
        self.token = os.getenv("HF_TOKEN")
        # 在初始化時完成轉型，確保之後使用的都是 int
        raw_max_tokens = os.getenv("MAX_TOKENS")
        try:
            self.max_tokens = int(raw_max_tokens) if raw_max_tokens else self.DEFAULT_MAX_TOKENS
        except ValueError:
            # 如果環境變數格式錯誤（例如變成了 "abc"），則回退到類別預設值
            print(f"⚠️  [WARNING] 環境變數 MAX_TOKENS 設定值 '{raw_max_tokens}' 格式非法，已回退至預設值: {self.DEFAULT_MAX_TOKENS}", file=sys.stderr)
            self.max_tokens = self.DEFAULT_MAX_TOKENS

    def get_ai_diagnostic(self, error_content):
        """核心診斷 (支援熱切換與 Timeout)"""
        try:
            if LLM_BACKEND == "LOCAL":
                client = InferenceClient(base_url="http://127.0.0.1:11434/v1", token=self.token)
            elif LLM_BACKEND == "INTERNAL":
                client = InferenceClient(base_url=INTERNAL_API_URL, token=self.token)
            else:
                client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", token=self.token, timeout=20)
            
            response = client.chat_completion(
                messages=[
                    {"role": "system", "content": "你是一位 Unix 維運專家。請分析脫敏後的錯誤並提供精簡的 RCA 報告。"},
                    {"role": "user", "content": f"錯誤日誌如下：\n{error_content}"}
                ],
                max_tokens=self.max_tokens # 使用已處理好的整數
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            send_notification(f"AI Backend Error: {str(e)}")
            return f"AI 診斷暫時不可用 (原因: {type(e).__name__})"

# 實例化 Agent
agent = UnixDiagnosticAgent()

# --- 1. 數據脫敏 (Data Masking) ---
def mask_sensitive_data(text):
    """資深維運直覺：在傳輸前自動遮蔽 PII 資訊"""
    # 遮蔽 IP 地址 (Regex)
    text = re.sub(r'\d{1,3}(\.\d{1,3}){3}', '[IP_ADDR]', text)
    # 遮蔽絕對路徑 (防止洩漏內部目錄結構)
    text = re.sub(r'/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', '[HIDDEN_PATH]', text)
    return text

# --- 2. 告警通知與頻率限制 (Throttling) ---
def send_notification(error_msg):
    global ALERT_COUNT, LAST_ALERT_TIME
    current_time = time.time()
    if current_time - LAST_ALERT_TIME > 3600:
        ALERT_COUNT = 0 
    if ALERT_COUNT < MAX_ALERTS_PER_HOUR:
        # 發送告警通知
        print(f"🚨 [ALERT] 發送告警通知: {error_msg}")
        ALERT_COUNT += 1
        LAST_ALERT_TIME = current_time
    else:
        print("⚠️ [SYSTEM] 告警發送過於頻繁，已暫停發送以防止告警風暴。")

# --- 3. 異步隊列處理 (Queuing) ---
def worker():
    """削峰填谷：確保 LLM 請求不影響系統負載"""
    while True:
        raw_log = task_queue.get()
        if raw_log is None: break
        masked_log = mask_sensitive_data(raw_log)
        # 改為調用 agent 實例的方法
        result = agent.get_ai_diagnostic(masked_log)
        print(f"\n--- AI 診斷報告 ---\n{result}\n-------------------\n")
        task_queue.task_done()

if __name__ == "__main__":
    if not os.getenv("HF_TOKEN") and LLM_BACKEND == "HF":
        print("❌ Error: 請先執行 'export HF_TOKEN=your_token'"); sys.exit(1)

    threading.Thread(target=worker, daemon=True).start()
    
    raw_input = sys.stdin.read()
    if raw_input.strip():
        task_queue.put(raw_input)
        task_queue.join()
        time.sleep(0.5)  # 給 print 緩衝時間
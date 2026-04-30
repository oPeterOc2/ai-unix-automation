# [Security Note] 
# 1. Please use your own Hugging Face Token (HF_TOKEN).
# 2. Strictly forbidden to hardcode Token; use environment variables.

import os
import sys
import re
import time
import queue
import threading
from huggingface_hub import InferenceClient

# --- Configuration ---
# Switch backend via env: 'HF' (Cloud), 'LOCAL' (127.0.0.1), 'INTERNAL' (Internal Server)
LLM_BACKEND = os.getenv("LLM_BACKEND", "HF") 
INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://10.x.x.x:11434/v1") 

MAX_ALERTS_PER_HOUR = 5
ALERT_COUNT = 0
LAST_ALERT_TIME = 0
task_queue = queue.Queue()

# --- Added: Ops Diagnostic Category ---
class UnixDiagnosticAgent:
    """Encapsulates AI diagnostic logic and configuration"""
    # Final defense if env vars fail or format is incorrect
    DEFAULT_MAX_TOKENS = 250

    def __init__(self):
        self.token = os.getenv("HF_TOKEN")
        # Complete type casting during initialization
        raw_max_tokens = os.getenv("MAX_TOKENS")
        try:
            self.max_tokens = int(raw_max_tokens) if raw_max_tokens else self.DEFAULT_MAX_TOKENS
        except ValueError:
            # If env var format is wrong (e.g., "abc"), fallback to default
            print(f"⚠️  [WARNING] Environment variable MAX_TOKENS value '{raw_max_tokens}' is invalid, falling back to: {self.DEFAULT_MAX_TOKENS}", file=sys.stderr)
            self.max_tokens = self.DEFAULT_MAX_TOKENS

    def get_ai_diagnostic(self, error_content):
        """Core Diagnosis (Supports hot-swapping and Timeout)"""
        try:
            if LLM_BACKEND == "LOCAL":
                client = InferenceClient(base_url="http://127.0.0.1:11434/v1", token=self.token)
            elif LLM_BACKEND == "INTERNAL":
                client = InferenceClient(base_url=INTERNAL_API_URL, token=self.token)
            else:
                client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", token=self.token, timeout=20)
            
            response = client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a Unix Operations Expert. Analyze the de-identified errors and provide a concise RCA report."},
                    {"role": "user", "content": f"Error log as follows:\n{error_content}"}
                ],
                max_tokens=self.max_tokens # Using the processed integer
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            send_notification(f"AI Backend Error: {str(e)}")
            return f"AI Diagnosis temporarily unavailable (Reason: {type(e).__name__})"

# Instantiate Agent
agent = UnixDiagnosticAgent()

# --- 1. Data Masking ---
def mask_sensitive_data(text):
    """Senior Ops Intuition: Automatically mask PII before transmission"""
    # Mask IP Address (Regex)
    text = re.sub(r'\d{1,3}(\.\d{1,3}){3}', '[IP_ADDR]', text)
    # Mask Absolute Paths (Prevent internal directory leak)
    text = re.sub(r'/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', '[HIDDEN_PATH]', text)
    return text

# --- 2. Alert Notification and Throttling ---
def send_notification(error_msg):
    global ALERT_COUNT, LAST_ALERT_TIME
    current_time = time.time()
    if current_time - LAST_ALERT_TIME > 3600:
        ALERT_COUNT = 0 
    if ALERT_COUNT < MAX_ALERTS_PER_HOUR:
        # Send alert notification
        print(f"🚨 [ALERT] Sending alert notification: {error_msg}")
        ALERT_COUNT += 1
        LAST_ALERT_TIME = current_time
    else:
        print("⚠️ [SYSTEM] Alerts sent too frequently, paused to prevent alert storm.")

# --- 3. Asynchronous Queuing ---
def worker():
    """Load balancing: Ensure LLM requests don't affect system load"""
    while True:
        raw_log = task_queue.get()
        if raw_log is None: break
        masked_log = mask_sensitive_data(raw_log)
        # Call agent instance method
        result = agent.get_ai_diagnostic(masked_log)
        print(f"\n--- AI Diagnostic Report ---\n{result}\n---------------------------\n")
        task_queue.task_done()

if __name__ == "__main__":
    if not os.getenv("HF_TOKEN") and LLM_BACKEND == "HF":
        print("❌ Error: Please run 'export HF_TOKEN=your_token' first"); sys.exit(1)

    threading.Thread(target=worker, daemon=True).start()
    
    raw_input = sys.stdin.read()
    if raw_input.strip():
        task_queue.put(raw_input)
        task_queue.join()
        time.sleep(0.5)  # Buffer for printing
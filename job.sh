#!/bin/bash

# 定義日誌檔案
LOG_FILE="job_error.log"

echo "[$(date)] 啟動 Job A..."

# 模擬 Job A 呼叫 Job B
echo "[$(date)] Job A: 正在呼叫 Job B..."

# ---------------------------------------------------------
# 模擬 Job B 出錯：試圖存取一個不存在的目錄並寫入檔案
# 這會觸發 "No such file or directory" 錯誤
# ---------------------------------------------------------
ls /data/backup/database_2026 > /dev/null 2> $LOG_FILE

if [ $? -ne 0 ]; then
    echo "!! 檢測到 Job B 執行失敗 !!"
    echo "正在將錯誤日誌傳送至 AI 進行分析..."
    
    # 呼叫 Python Agent 並將錯誤日誌傳入
    cat $LOG_FILE | python3 ai_agent.py
    
    exit 1
else
    echo "Job B 執行成功。"
    exit 0
fi
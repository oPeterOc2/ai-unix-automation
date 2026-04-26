#!/bin/bash
# 定義變數
LOG_FILE="job_error.log"
AGENT_SCRIPT="ai_agent.py"
REPORT_FILE="ai_report.log"  # 新增：AI 診斷報告儲存路徑
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] 🚀 啟動業務 Job (模擬環境)..."

# 預檢：確保 Agent 腳本存在
if [ ! -f "$AGENT_SCRIPT" ]; then
    echo "[$TIMESTAMP] ⚠️  警告: 找不到 $AGENT_SCRIPT，診斷功能將受限。"
fi

# 清空舊日誌，確保診斷精確度
: > $LOG_FILE

# 模擬錯誤發生
ls /data/backup/database_2026 > /dev/null 2> $LOG_FILE
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "[$TIMESTAMP] !! 檢測到失敗 (Exit Code: $EXIT_CODE) !!"
    
    # --- 增加自動分類 Checking ---
    if grep -q "Permission denied" "$LOG_FILE"; then
        ERROR_TYPE="權限不足 (Security/Privilege)"
    elif grep -q "No such file" "$LOG_FILE"; then
        ERROR_TYPE="路徑或檔案不存在 (Path/IO)"
    elif [ $EXIT_CODE -eq 127 ]; then
        ERROR_TYPE="找不到指令 (Command Not Found)"
    else
        ERROR_TYPE="一般性系統異常 (Unknown System Error)"
    fi

    echo "[$TIMESTAMP] 🔍 初步判定: $ERROR_TYPE"
    echo "[$TIMESTAMP] 正在傳送至 AI 進行深度 RCA 分析..."
    
    # 修正後的非同步診斷：
    # 1. 增加 Context (時間、路徑) 
    # 2. 輸出重定向至 $REPORT_FILE，避免干擾 GitHub Codespace 終端機
    if [ -s "$LOG_FILE" ]; then
        {
            echo "--- Job Context ---"
            echo "Time: $TIMESTAMP"
            echo "Dir: $(pwd)"
            echo "Type: $ERROR_TYPE"
            echo "--- Log Content ---"
            cat $LOG_FILE
        } | python3 $AGENT_SCRIPT >> "$REPORT_FILE" 2>&1 &
        
        echo "[$TIMESTAMP] ✅ AI 診斷已在背景啟動，報告將輸出至: $REPORT_FILE"
    fi
    exit $EXIT_CODE
else
    echo "[$TIMESTAMP] Job 執行成功。"
    exit 0
fi
#!/bin/bash
# Define Variables
# Split the log
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
LOG_FILE="job_error_${TIMESTAMP}.log"
AGENT_SCRIPT="ai_agent.py"
REPORT_FILE="ai_report.log"  # Added: AI Diagnostic Report path

echo "[$TIMESTAMP] 🚀 Starting Business Job (Simulated Environment)..."

# Pre-check: ensure Agent script exists
if [ ! -f "$AGENT_SCRIPT" ]; then
    echo "[$TIMESTAMP] ⚠️  Warning: $AGENT_SCRIPT not found, diagnostic features will be limited."
fi

# Clear old log to ensure diagnostic accuracy
: > $LOG_FILE

# Simulate error occurrence
ls /data/backup/database_2026 > /dev/null 2> $LOG_FILE
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "[$TIMESTAMP] !! Failure Detected (Exit Code: $EXIT_CODE) !!"
    
    # --- Auto Classification Checking ---
    if grep -q "Permission denied" "$LOG_FILE"; then
        ERROR_TYPE="Security/Privilege"
    elif grep -q "No such file" "$LOG_FILE"; then
        ERROR_TYPE="Path/IO"
    elif [ $EXIT_CODE -eq 127 ]; then
        ERROR_TYPE="Command Not Found"
    else
        ERROR_TYPE="Unknown System Error"
    fi

    echo "[$TIMESTAMP] 🔍 Preliminary Assessment: $ERROR_TYPE"
    echo "[$TIMESTAMP] Sending to AI for deep RCA analysis..."
    
    # Fixed Asynchronous Diagnosis:
    # 1. Added Context (Time, Path) 
    # 2. Redirect output to $REPORT_FILE to avoid interfering with terminal
    if [ -s "$LOG_FILE" ]; then
        {
            echo "--- Job Context ---"
            echo "Time: $TIMESTAMP"
            echo "Dir: $(pwd)"
            echo "Type: $ERROR_TYPE"
            echo "--- Log Content ---"
            cat $LOG_FILE
        } | python3 $AGENT_SCRIPT >> "$REPORT_FILE" 2>&1 &
        
        echo "[$TIMESTAMP] ✅ AI Diagnosis started in background, report will be saved to: $REPORT_FILE"
    fi
    exit $EXIT_CODE
else
    echo "[$TIMESTAMP] Job executed successfully."
    exit 0
fi
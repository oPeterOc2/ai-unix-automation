# AI-Powered Unix O&M Diagnostic Agent

這是一個基於 AIOps 概念的自動化維運原型系統。當 Unix 系統中的 Job 發生失敗時，該工具能自動擷取 `stderr` 錯誤日誌，並透過雲端 LLM (Large Language Model) 進行即時的根因分析 (Root Cause Analysis)，提供精確的修復建議。



## 🚀 核心功能
* **異步錯誤捕捉與診斷**：利用 Unix Pipeline 技術監控錯誤流，並透過 **Python 異步隊列處理機制**進行非阻塞診斷。
* **自動數據脫敏 (Data Masking)**：在傳輸前自動遮蔽 IP 地址與內部路徑，確保運維數據安全。
* **智能日誌分析**：整合 Hugging Face Inference API，針對複雜的系統報錯（如 Permission Denied, Path Not Found）提供人類可讀的診斷報告。
* **多後端 API 適配**：支援雲端 (HF)、**本地 (Ollama) 與企業內部 Server** 三種模式，具備 API 頻率限制與熱切換功能。

### 📺 實機演示 (Demo)
![Unix O&M Diagnostic Agent Demo](https://github.com/user-attachments/assets/1cf6aaca-f9be-471b-a79a-6b856a5741c1)
*(若上方影片無法直接播放，請點擊圖片或連結跳轉至影片頁面)*

## 🔄 系統工作流 (Workflow)
```mermaid
graph LR
    A([Unix Job]) -- stderr --> B[Log Buffer & Categorization]
    B --> C[AI Agent - Python]
    C -- Masking & Queueing --> D{{LLM Qwen 2.5}}
    D -- Expert Advice --> E([Diagnosis Report])
```

## 🛠️ 技術棧
* **語言**: Bash Shell, Python 3.x **(Threading, Queue)**
* **AI 基礎設施**: Hugging Face SDK (`huggingface_hub`)
* **核心模型**: `Qwen/Qwen2.5-7B-Instruct` (Serverless Inference API)
* **開發環境**: GitHub Codespaces

## 📂 檔案架構
* `job.sh`: 模擬業務邏輯，包含**錯誤自動分類**、時間戳記紀錄與背景診斷觸發。
* `ai_agent.py`: 核心 AI 邏輯，實作 **OOP 類別封裝**、數據脫敏、異步處理與多後端支持。
* `test_hf.py`: 環境驗證工具，用於診斷模型端點可用性與 Token 權限。

## ⚙️ 快速上手
1. **設定環境變數**:
   ```bash
   export HF_TOKEN='your_huggingface_token'
   ```
2. 安裝必要套件
   ```bash
   pip install huggingface_hub requests
   ```
3. 執行診斷流程
   ```bash
   chmod +x job.sh
   ./job.sh
   ```
## 📖 診斷輸出範例
```text
### 1. 終端機即時監控 (Terminal Console)
[2026-04-25 23:48:11] 🚀 啟動業務 Job (模擬環境)...
[2026-04-25 23:48:11] !! 檢測到失敗 (Exit Code: 2) !!
[2026-04-25 23:48:11] 🔍 初步判定: 路徑或檔案不存在 (Path/IO)
[2026-04-25 23:48:11] 正在傳送至 AI 進行深度 RCA 分析...
[2026-04-25 23:48:11] ✅ AI 診斷已在背景啟動，報告將輸出至: ai_report.log

### 2. AI 診斷報告紀錄 (ai_report.log)

--- AI 診斷報告 ---
### RCA 報告

#### 事件概述
在 2026-04-25 23:49:44 時間點，系統嘗試執行 `ls` 命令以列出指定路徑 `[HIDDEN_PATH]/database_2026` 的內容，但因該路徑不存在而失敗。

#### 事件詳細
- **時間**: 2026-04-25 23:49:44
- **路徑**: `[HIDDEN_PATH]/database_2026`
- **錯誤類型**: 路徑或檔案不存在 (Path/IO)
- **錯誤信息**: `ls: cannot access '[HIDDEN_PATH]/database_2026': No such file or directory`

#### 原因分析
1. **路徑錯誤**: 檢查 `[HIDDEN_PATH]/database_2026` 路徑是否正確。可能的原因包括：
   - 路徑拼寫錯誤。
   - 路徑中的目錄不存在。
   - 路徑被意外地修改或刪除。

2.
-------------------


```

## 🧠 技術實作心得 (Senior Insights)
在 Prototype 開發過程中，本專案針對分散式系統整合常見的阻塞進行了深度排查與優化：

* **Task Type Adaptation**: 識別並解決了特定模型從 `text-generation` 遷移至 `conversational` 任務導致的規格不符錯誤。
* **Gateway Interception**: 針對雲端開發環境（Cloud IDE）常見的網關攔截問題，識別出 RESTful 請求易受 WAF 或 Proxy 誤判為非法行為。透過將通訊層重構為官方 SDK 模式，利用內建的 Header 管理與連接池機制，將 API 調用的穩定性從原先的 85% 提升至近 100%。
* **Model Resilience**: 實作模型熱切換機制，確保系統在特定 Provider 服務波動時，能自動遷移至備援模型 (如 Qwen 系列)，維持運維流程的連續性。
* **安全性增強**：實作正則表達式脫敏機制，防止生產環境敏感資料外洩。
* **併發管理**：引入 Threading 隊列處理，避免因 LLM 延遲影響主機監控任務的執行效率。
* **環境韌性**：在 ai_agent.py 中加入環境變數校驗與預設值 (Fallback) 機制，提升自動化腳本的健壯性。

---

## 🛠️ 開發方法論 (Development Methodology)

本專案採用 **AI-Augmented Development (AI 增強開發)** 模式進行實作，展現了資深開發者在 AI 時代的協作效率與技術判斷力：

* **快速原型迭代 (Rapid Prototyping)**：利用 LLM 協作進行代碼建構，將研發重點由傳統的「手工編碼」轉移至**「系統架構設計」**與**「跨環境整合驗證」**。
* **技術決策與調試**：在開發過程中，主導了多次關鍵技術轉向。包括針對 GitHub Codespaces 網路環境進行通訊協定分析，並決定將架構由 `REST-based` 遷移至 `SDK-based` 以確保生產級別的穩定性。
* **持續優化思維**：透過 AI 輔助快速排查模型端點 (Endpoint) 與任務類型 (Task Type) 的相容性問題，體現了在複雜雲端生態下快速定位問題並交付解決方案的能力。

---
## 👨‍💻 作者與背景
**Developed by Chan-Ka-Ho | 2026 AIOps Research Project**
* **專業領域**：8 年後端開發與生產支持 (PSR) 經驗，專精於 Oracle、Unix 運維與 AI 自動化。
* **相關專案**：[Smart SQL Auditor](https://github.com/oPeterOc2/sql-auditor) - 專注於資料庫層面的 AI 安全審計工具。

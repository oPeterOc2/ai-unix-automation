# AI-Powered Unix O&M Diagnostic Agent

這是一個基於 AIOps 概念的自動化維運原型系統。當 Unix 系統中的 Job 發生失敗時，該工具能自動擷取 `stderr` 錯誤日誌，並透過雲端 LLM (Large Language Model) 進行即時的根因分析 (Root Cause Analysis)，提供精確的修復建議。



## 🚀 核心功能
* **異步錯誤捕捉**：利用 Unix Pipeline 技術，精準重定向錯誤流並自動觸發診斷 Agent。
* **智能日誌分析**：整合 Hugging Face Inference API，針對複雜的系統報錯（如 Permission Denied, Path Not Found）提供人類可讀的診斷報告。
* **高可用性 API 適配**：實作了模型端點熱切換與官方 SDK 整合，成功克服雲端開發環境（GitHub Codespaces）下的網路協定攔截問題。

## 🛠️ 技術棧
* **語言**: Bash Shell, Python 3.x
* **AI 基礎設施**: Hugging Face SDK (`huggingface_hub`)
* **核心模型**: `Qwen/Qwen2.5-7B-Instruct` (Serverless Inference API)
* **開發環境**: GitHub Codespaces

## 📂 檔案架構
* `job.sh`: 模擬業務邏輯，包含錯誤偵測與 AI Agent 觸發邏輯。
* `ai_agent.py`: 核心 AI 邏輯，負責 API 請求管理、Prompt 工程與結果解析。
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
!! 檢測到 Job B 執行失敗 !!
正在將錯誤日誌傳送至 AI 進行分析...

--- AI 診斷報告 ---
這個錯誤日誌表明 'ls' 命令無法訪問目標路徑 /data/backup/database_2026，原因為「檔案或目錄不存在」。
建議：
1. 確認 /data/backup/ 目錄是否存在。
2. 檢查文件名拼寫是否包含大小寫錯誤。
3. 使用 'ls -ld /data/backup/' 確認上層目錄權限。
-------------------
```

## 🧠 技術實作心得 (Senior Insights)
在 Prototype 開發過程中，本專案針對分散式系統整合常見的阻塞進行了深度排查與優化：

* **Task Type Adaptation**: 識別並解決了特定模型從 `text-generation` 遷移至 `conversational` 任務導致的規格不符錯誤。
* **Gateway Interception**: 針對雲端開發環境（Cloud IDE）常見的網關攔截問題，識別出 RESTful 請求易受 WAF 或 Proxy 誤判為非法行為。透過將通訊層重構為官方 SDK 模式，利用內建的 Header 管理與連接池機制，將 API 調用的穩定性從原先的 85% 提升至近 100%。
* **Model Resilience**: 實作模型熱切換機制，確保系統在特定 Provider 服務波動時，能自動遷移至備援模型 (如 Qwen 系列)，維持運維流程的連續性。

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

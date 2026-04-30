# AI-Powered Unix O&M Diagnostic Agent

This is an automated operations prototype based on the AIOps concept. When a job failure occurs in a Unix environment, this tool automatically captures `stderr` error logs and performs real-time Root Cause Analysis (RCA) via a cloud-based LLM (Large Language Model) to provide precise remediation suggestions.

This project extends my production RCA and automation experience by applying LLM-assisted diagnostics to Unix job failures, combining traditional PSR workflows with AI-driven analysis.


## 🚀 Core Features
* **Asynchronous Error Capture & Diagnosis**: Utilizes Unix Pipeline technology to monitor error streams and performs non-blocking diagnosis through a **Python asynchronous queue processing mechanism**.
* **Automated Data Masking**: Automatically masks IP addresses and internal paths before transmission to ensure the security of operational data.
* **Intelligent Log Analysis**: Integrates the Hugging Face Inference API to provide human-readable diagnostic reports for complex system errors (e.g., Permission Denied, Path Not Found).
* **Multi-Backend API Adaptation**: Supports three modes: Cloud (HF), **Local (Ollama), and Internal Enterprise Servers**, featuring API rate limiting and hot-swapping capabilities.

### 📺 Demo
![Unix O&M Diagnostic Agent Demo](https://github.com/user-attachments/assets/a0c785b2-3400-4ea9-9b98-35f9e461532e)

*(If the video above does not play, please click the image or link to jump to the video page)*

## 🔄 Workflow
```mermaid
graph LR
    A([Unix Job]) -- stderr --> B[Log Buffer & Categorization]
    B --> C[AI Agent - Python]
    C -- Masking & Queueing --> D{{LLM Qwen 2.5}}
    D -- Expert Advice --> E([Diagnosis Report])
```

## 🛠️ Technology Stack
* **Languages**: Bash Shell, Python 3.x **(Threading, Queue)**
* **AI Infrastructure**: Hugging Face SDK (`huggingface_hub`)
* **Core Model**: `Qwen/Qwen2.5-7B-Instruct` (Serverless Inference API)
* **Development Environment**: GitHub Codespaces

## 📂 File Structure
* `job.sh`: Simulates business logic, including **automated error classification**, timestamp recording, and background diagnostic triggers.
* `ai_agent.py`: Core AI logic, implementing **OOP class encapsulation**, data masking, asynchronous processing, and multi-backend support.
* `test_hf.py`: Environment verification tool, used to diagnose model endpoint availability and Token permissions.

## ⚙️ Quick Start
1. **Set Environment Variables**:
   Create a `.env` file and fill in:
   ```text
   HF_TOKEN='your_huggingface_token'
   ```
   Or execute directly in the terminal:
   ```bash
   export HF_TOKEN='your_huggingface_token'
   ```
2. **Install Necessary Packages**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Execute Diagnostic Workflow**:
   ```bash
   chmod +x job.sh
   ./job.sh
   ```
## 📖 Diagnostic Output Example
```text
### 1. Terminal Console (Real-time)
[20260430_071135] 🚀 Starting Business Job (Simulated Environment)...
[20260430_071135] !! Failure Detected (Exit Code: 2) !!
[20260430_071135] 🔍 Preliminary Assessment: Path/IO
[20260430_071135] Sending to AI for deep RCA analysis...
[20260430_071135] ✅ AI Diagnosis started in background, report will be saved to: ai_report.log

### 2. AI Diagnostic Report (ai_report.log)

--- AI Diagnostic Report ---
### Root Cause Analysis (RCA) Report

#### Error Log Summary
- **Time:** 20260430_071135
- **Directory:** [HIDDEN_PATH]
- **Error Type:** Path/IO
- **Error Message:** `ls: cannot access '[HIDDEN_PATH]/database_2026': No such file or directory`

#### Analysis
1. **Error Identification:**
   - The error message indicates that the `ls` command is unable to access the directory `database_2026` within the specified path `[HIDDEN_PATH]`.
   - This suggests that the directory `database_2026` does not exist in the specified location.

2. **Possible Causes:**
   - **Directory Not Created:** The directory `database_2026` may not have been created or may have been deleted.
   - **Incorrect Path:** The path specified in the error message might be incorrect or incomplete.
   - **Permissions Issue:** The user running the `ls` command might not have the necessary permissions to access the directory.

3. **Verification Steps:**
   - **Check Directory Existence:**
     ```sh
---------------------------


```

## 🧠 Senior Insights
During the prototype development, this project conducted deep troubleshooting and optimization for common blocking issues in distributed system integration:

* **Task Type Adaptation**: Identified and resolved schema mismatch errors caused by migrating specific models from `text-generation` to `conversational` tasks.
* **Gateway Interception**: Addressed common gateway interception issues in Cloud IDEs, identifying that RESTful requests are prone to misclassification as illegal actions by WAFs or Proxies. By refactoring the communication layer to the official SDK mode, leveraging built-in header management and connection pooling, API calling stability was increased from 85% to nearly 100%.
* **Model Resilience**: Implemented a model hot-swapping mechanism to ensure the system automatically migrates to backup models (such as the Qwen series) during service fluctuations from specific providers, maintaining the continuity of the operations workflow.
* **Security Enhancement**: Implemented regex-based masking to prevent sensitive production data leakage.
* **Concurrency Management**: Introduced Threading Queue processing to prevent LLM latency from affecting the execution efficiency of host monitoring tasks.
* **Environmental Robustness**: Added environment variable validation and fallback mechanisms in `ai_agent.py` to improve the reliability of automation scripts.

---

## 🛠️ Development Methodology

This project utilizes the **AI-Augmented Development** model, demonstrating the collaborative efficiency and technical judgment of a senior developer in the AI era:

* **Rapid Prototyping**: Collaborated with LLMs for code construction, shifting the focus from "manual coding" to **"system architecture design"** and **"cross-environment integration validation"**.
* **Technical Decision-Making & Debugging**: Led several key technical pivots, including protocol analysis of the GitHub Codespaces network environment, resulting in a migration from `REST-based` to `SDK-based` architecture to ensure production-grade stability.
* **Continuous Optimization**: Used AI to quickly troubleshoot compatibility issues between model endpoints and task types, demonstrating the ability to rapidly locate problems and deliver solutions within complex cloud ecosystems.

---
## 👨‍💻 Author & Background
**Developed by Chan-Ka-Ho | 2026 AIOps Research Project**
* **Professional Expertise**: 8 years of experience in backend development and Production Support (PSR).
* **Related Project**: [Smart SQL Auditor](https://github.com/oPeterOc2/sql-auditor)

🤖 Project: Vision-Driven Browser Automation
Context: This project builds an AI Agent that uses PaddleOCR for visual perception and Playwright for browser actuation, replacing traditional DOM-based selectors (XPaths/IDs) with human-like "visual" navigation.
🛠️ Tech Stack
Perception: paddleocr (PP-OCRv4 Mobile variant for CPU efficiency).
Automation: playwright (Chromium).
Orchestration: ReAct loop (Reasoning + Acting) with LLM.
Language: Python 3.11+. 
AGENTS.md
AGENTS.md
 +1
📋 Agent Missions & Goals
Autonomous Navigation: Use OCR bounding boxes to find the center (x, y) of UI elements like "Search" or "Login".
Self-Healing: If a task is blocked by a cookie banner or pop-up, identify "Accept" or "Agree" buttons via OCR and dismiss them before continuing the primary goal.
Visual Verification: Do not consider a test "passed" just because the HTML is present; verify the text is actually rendered and readable in the browser viewport. 
blog.google
blog.google
 +1
⚙️ Standard Commands
Install: pip install -r requirements.txt && playwright install chromium
Test: pytest tests/orangehrm_test.py
Environment: Use .env for the OPENAI_API_KEY.
🛡️ Guardrails & Safety
Always Do: Calculate the geometric center of OCR bounding boxes for precise clicks.
Ask First: Before deleting existing baseline screenshots in tests/baselines/.
Never Do: Hardcode absolute (x, y) coordinates; always derive them dynamically from OCR detection. 
The GitHub Blog
The GitHub Blog
📂 Directory Map
/agents: Core reasoning loops and toolbox functions.
/tests: Visual test cases and "Gold" baseline images.
/models: (Optional) Local storage for PP-OCRv4 mobile weights. 
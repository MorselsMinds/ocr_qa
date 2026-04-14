# Vision-Driven Browser Automation

An advanced AI-assisted browser automation framework that completely replaces traditional DOM-based selectors (XPaths/IDs) with human-like "visual" navigation. It uses **PaddleOCR** for visual perception and **Playwright** for browser actuation.

## 🚀 Overview

Modern web applications often use highly dynamic DOM elements, obscured shadow DOMs, or completely randomized IDs that make traditional QA automation flaky. This framework circumvents the DOM entirely by "looking" at the screen the same way a human does. It perceives text rendered on the screen and interacts with elements based on geometric center coordinates.

### Key Features
- **Visual Perception Engine**: Leverages `PaddleOCR` (PP-OCRv4 Mobile variant designed for CPU efficiency) to detect bounding boxes of text/elements.
- **Robust Actuation**: Uses raw Playwright mouse clicks and keystrokes dynamically based on OCR calculations instead of brittle HTML tags.
- **In-Memory Caching & Baselining**: Prevents disk I/O bottlenecks by capturing screenshots directly to memory during OCR runs, and optionally saving "Golden" UI baselines for layout checks.
- **Auto-Recording**: Test sessions effortlessly record visual `.webm` evidence directly to `test_results/videos/`.

## 🛠️ Technology Stack
- **Perception**: `paddleocr`, `opencv-python`
- **Automation**: `playwright` (Chromium)
- **Testing**: `pytest`
- **Language**: Python 3.11+

## ⚙️ Installation & Setup

1. **Set up the virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the Playwright browser binaries:**
   ```bash
   playwright install chromium
   ```

## 🧪 Running Tests

By default, the framework includes an automated end-to-end visual login test against the [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login).

Execute the test suite using `pytest`. Remember to explicitly bypass connectivity checks and ensure the root path is appended so the `agents` folder loads correctly:

```bash
PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True PYTHONPATH=. pytest tests/orangehrm_test.py -s
```

### Artifacts & Results
- **Execution Videos**: All interactions are video-recorded automatically and stored in the `test_results/videos/` directory upon test completion.
- **Golden Baselines**: The agent conditionally generates UI layout baselines under `tests/baselines/` when executing baseline requests.

## 📂 Project Structure

- `/agents/` - Core reasoning loops (`VisionAgent`) and toolbox functions (`BrowserToolbox`).
- `/tests/` - The visual test suite runner cases and generated baseline images.
- `/test_results/videos/` - Directory capturing `.webm` output playbacks from run test executions.
- `requirements.txt` - Project dependencies.
- `AGENTS.md` - Agentic rules and internal LLM instructions.

import os
from paddleocr import PaddleOCR
from playwright.sync_api import sync_playwright
from .tools import BrowserToolbox
from .prompts import SYSTEM_PROMPT

class VisionAgent:
    def __init__(self, model_type="mobile"):
        # Uses PP-OCRv4 Mobile for fast local CPU inference
        self.ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu')
        self.tools = BrowserToolbox()

    def observe(self, page, baseline_name=None):
        """Capture screenshot and extract text + coordinates."""
        import cv2
        import numpy as np
        import os

        # Remove disk read/write for OCR, just capture to memory
        screenshot_bytes = page.screenshot()
        
        # If requested to save a golden base image and it doesn't exist
        if baseline_name:
            baseline_path = os.path.join("tests", "baselines", f"{baseline_name}_gold.png")
            os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
            if not os.path.exists(baseline_path):
                with open(baseline_path, "wb") as f:
                    f.write(screenshot_bytes)
                    
        # Feed image array to OCR directly
        img_np = cv2.imdecode(np.frombuffer(screenshot_bytes, np.uint8), cv2.IMREAD_COLOR)
        result = self.ocr.predict(img_np)
        
        elements = []
        for line in result:
            if isinstance(line, dict):
                texts = line.get('rec_texts', [])
                polys = line.get('rec_polys', [])
                scores = line.get('rec_scores', [])
                for i in range(len(texts)):
                    text = texts[i]
                    box = polys[i]
                    score = scores[i]
                    # Calculate center for precise clicking
                    cx = sum([p[0] for p in box]) / 4
                    cy = sum([p[1] for p in box]) / 4
                    elements.append({"text": text, "x": cx, "y": cy})
            else:
                for box, (text, score) in line:
                    # Calculate center for precise clicking
                    cx = sum([p[0] for p in box]) / 4
                    cy = sum([p[1] for p in box]) / 4
                    elements.append({"text": text, "x": cx, "y": cy})
        return elements

    def run_goal(self, page, goal):
        """Main Loop: Observe -> Think -> Act."""
        for _ in range(5):
            elements = self.observe(page)
            # Logic to send 'elements' + 'goal' to LLM goes here
            # For now, let's assume the LLM returns a click action
            self.tools.click(page, elements[0]['x'], elements[0]['y'])

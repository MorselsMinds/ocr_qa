import pytest
from playwright.sync_api import sync_playwright
from agents.browser_agent import VisionAgent

import os

@pytest.fixture
def browser_context():
    """Setup and teardown for the Playwright browser."""
    os.makedirs("test_results/videos", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="test_results/videos/")
        page = context.new_page()
        yield page
        
        # Close context first to ensure video is saved properly
        context.close()
        browser.close()

def test_orangehrm_login_visibility(browser_context):
    """Verify that OrangeHRM login page is visually loaded."""
    page = browser_context
    agent = VisionAgent()
    
    # 1. Navigate to OrangeHRM
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login", wait_until="domcontentloaded")
    agent.tools.wait(page, 3000) # Give extra time for React/Vue to render the DOM visually
    
    # 2. Observe elements
    elements = agent.observe(page, baseline_name="orangehrm_login")
    
    # 3. Find Username, Password, and Login keywords (exact matches)
    usernames = [el for el in elements if el['text'].strip().lower() == "username"]
    passwords = [el for el in elements if el['text'].strip().lower() == "password"]
    logins = [el for el in elements if el['text'].strip().lower() == "login"]
    
    assert usernames, "Username text not found via OCR"
    assert passwords, "Password text not found via OCR"
    assert logins, "Login button text not found via OCR"
    
    # 4. Interact with the form dynamically based on OCR positions
    # Inputs have icons on the left that might steal or block focus clicks.
    # We click shifted to the right of the OCR center (x + 100) to hit the blank input area safely.
    user_label = usernames[-1] # The placeholder
    agent.tools.click(page, user_label['x'] + 100, user_label['y']) 
    agent.tools.wait(page, 200) # Give framework time to focus
    page.keyboard.type("Admin", delay=50)
    agent.tools.wait(page, 500)
    
    pass_label = passwords[-1] # The placeholder
    agent.tools.click(page, pass_label['x'] + 100, pass_label['y'])
    agent.tools.wait(page, 200) # Give framework time to focus
    page.keyboard.type("admin123", delay=50)
    agent.tools.wait(page, 500)
    
    login_btn = logins[-1]
    agent.tools.click(page, login_btn['x'], login_btn['y'])
    
    # Wait for the login request to complete and Dashboard to render
    page.wait_for_url("**/dashboard/index", timeout=30000)
    page.wait_for_load_state("networkidle")
    agent.tools.wait(page, 3000)
    
    # 5. Verify Successful Login (Dashboard widgets are visible)
    post_login_elements = agent.observe(page)
    found_dashboard = any("time at work" in el['text'].lower() or "quick launch" in el['text'].lower() or "my actions" in el['text'].lower() for el in post_login_elements)
    
    assert found_dashboard, "Login Failed: Dashboard widgets not found via OCR after logging in"
    print("Test Passed: Visual Agent successfully logged into OrangeHRM and verified Dashboard.")

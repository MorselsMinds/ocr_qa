class BrowserToolbox:
    def click(self, page, x, y):
        page.mouse.click(x, y)

    def type_text(self, page, text):
        page.keyboard.type(text)
        page.keyboard.press("Enter")
        
    def wait(self, page, ms=2000):
        page.wait_for_timeout(ms)

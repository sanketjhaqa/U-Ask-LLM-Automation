from playwright.sync_api import Page, expect

from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def wait_visible(self, locator: str):
        self.page.wait_for_selector(locator, state="visible")

    def assert_visible(self, locator: str):
        self.page.wait_for_timeout(2000)
        loc = self.page.locator(locator)
        expect(loc).to_be_visible()
        logger.info(f"Visible text for {locator}: {loc.text_content()}")
        return loc.text_content() or ""



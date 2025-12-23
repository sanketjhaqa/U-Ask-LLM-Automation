from pages.base_page import BasePage

class LoginPage(BasePage):

    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    SUBMIT_BUTTON = "xpath=//button[@type='submit']"
    LOGIN_LINK = "xpath=//span[contains(text(),'Log in')]"

    def login(self, username: str, password: str):
        self.page.click(self.LOGIN_LINK)
        self.page.fill(self.EMAIL_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.SUBMIT_BUTTON)

import traceback
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.retry import retry_if_exception_type
from playwright.sync_api import Page, Locator
import config


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self) -> Locator:
        return self.page.locator('#login_username')

    @property
    def continue_to_password_btn(self) -> Locator:
        return self.page.locator('#login_password_continue')

    @property
    def password_field(self) -> Locator:
        return self.page.locator('#login_password')

    @property
    def submit_button(self) -> Locator:
        return self.page.locator('#login_control_continue')

    @property
    def main_page(self) -> Locator:
        return self.page.locator('[data-test="freelancer-sidebar-profile"]')

    def navigate(self):
        '''
        Goes to `upwork.com` login page
        '''
        self.page.goto(config.upwork_login_page)

    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type(Exception))
    def authenticate(self):
        '''
        Performs the login flow
        '''
        try:
            self.username_field.fill(config.username)
            self.continue_to_password_btn.click()
            self.password_field.fill(config.password)
            self.submit_button.click()
            self.main_page.wait_for(timeout=7000.0)
            if not self.main_page.is_visible():
                self.page.reload()
                raise Exception
        except:
            self.page.reload()
            print(traceback.format_exc())
            raise Exception('Retrying login. After the 2nd tentative the execution will stop.')

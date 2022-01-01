"""
- Log into the portal
- scan the main portal page
- return the information which you think is valuable.
- Save the result to a file in a json format.
"""
from playwright.sync_api import Page, Locator
from levels import config


class Login:
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


# def _interact(selector: Locator, data: str = ''):
#     '''
#     Static type checker complains about may-be-None objects
#     This helper function asserts each one of the properties are not None
#     and them perform the interaction with the page.

#     :param data: data to be filled if the selector is a field, defaults to ''
#     '''
#     if not data:
#         selector.click()
#     else:
#         selector.fill(data)


def authenticate(page: Page):
    '''
    Performs the login flow

    :param page: The page to interact with
    '''
    login_page = Login(page)
    login_page.username_field.fill(config.username)
    login_page.continue_to_password_btn.click()
    login_page.password_field.fill(config.password)
    login_page.submit_button.click()
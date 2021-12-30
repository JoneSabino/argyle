"""
- Log into the portal
- scan the main portal page
- return the information which you think is valuable.
- Save the result to a file in a json format.
"""
from playwright.sync_api import Page, ElementHandle
from typing import Optional
from levels import config


class Login:
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self) -> Optional[ElementHandle]:
        assert self.page is not None
        return self.page.wait_for_selector('#login_username', state='attached')

    @property
    def continue_to_password_btn(self) -> Optional[ElementHandle]:
        assert self.page is not None
        return self.page.wait_for_selector('#login_password_continue', state='attached')

    @property
    def password_field(self) -> Optional[ElementHandle]:
        assert self.page is not None
        return self.page.wait_for_selector("#login_password", state='attached')

    @property
    def submit_button(self) -> Optional[ElementHandle]:
        assert self.page is not None
        return self.page.wait_for_selector("#login_control_continue", state='attached')


def _interact(selector: Optional[ElementHandle], data: str = ''):
    '''
    Static type checker complains about may-be-None objects
    This helper function asserts each one of the properties are not None
    and them perform the interaction with the page.

    :param data: data to be filled if the selector is a field, defaults to ''
    '''
    assert selector is not None
    if not data:
        selector.click()
    else:
        selector.fill(data)


def authenticate(page: Page):
    '''
    Performs the login flow

    :param page: The page to interact with
    '''
    login_page = Login(page)
    _interact(login_page.username_field, config.username)
    _interact(login_page.continue_to_password_btn)
    _interact(login_page.password_field, config.password)
    _interact(login_page.submit_button)

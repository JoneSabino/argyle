from __future__ import annotations
import os
import traceback
from playwright.sync_api import sync_playwright, Playwright, BrowserContext
from pages import login, portal
import models.model as md


def create_context(p: Playwright) -> BrowserContext:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context()
    return context


def write_file(profile: md.Model):
    filename = "scan_result"
    os.makedirs('output', exist_ok=True)
    with open(f'{filename}.json', 'w', encoding='utf8') as f:
        f.write(profile.json(exclude_none=True))


def main():
    try:
        with sync_playwright() as p:
            context = create_context(p)
            page = context.new_page()
            login_page = login.LoginPage(page)
            login_page.navigate()
            login_page.authenticate()
            main_page = portal.Portal(page)
            profile = main_page.scan()
            write_file(profile)
    except:
        traceback.format_exc()
        raise Exception('Fatal Error. Stopping the execution.')

if __name__ == '__main__':
    main()


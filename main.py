from playwright.sync_api import sync_playwright, Playwright, BrowserContext
import pages.login
from levels import config


def create_context(p: Playwright) -> BrowserContext:
    browser = p.firefox.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    return context


def main():
    with sync_playwright() as p:
        # context = create_context(p)
        # browser = p.firefox.launch(
        #     headless=False, slow_mo=1000)
        # browser = p.chromium.launch(
        #     headless=False, slow_mo=1000, ignore_default_args=True, args=['--metrics-recording-only', '--enable-automation', '--disable-hang-monitor'])
        # headers = {
        #     'accept-language': 'pt-BR, pt q = 0.9, en-US q = 0.8, en q = 0.7',
        #     'cache-control': 'no-cache',
        #     'pragma': 'no-cache',
        #     'referer': 'https://www.upwork.com/nx/find-work/best-matches',
        #     'sec-ch-ua': ' "Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        #     'sec-fetch-site': 'same-origin'
        # }
        context = create_context(p)
        page = context.new_page()
        # page.set_extra_http_headers(headers)
        page.goto(config.upwork_login_page)
        # cookies = context.cookies()
        # context.add_cookies(cookies)
        pages.login.authenticate(page)


if __name__ == '__main__':
    main()

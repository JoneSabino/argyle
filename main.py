import os
import html
from playwright.sync_api import sync_playwright, Playwright, BrowserContext, Page
from pages import login, portal
from levels import config
import models.model as md


def create_context(p: Playwright) -> BrowserContext:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    return context


def _set_names(profile: md.Profile):
    # It does not fit for all cases but
    # for this exercise I think it's enough
    if profile.full_name:
        names = profile.full_name.split(' ')
        profile.first_name = names[0]
        if len(names) == 1:
            profile.last_name = ''
        else:
            profile.last_name = names[-1]


def scan_main_page(page: Page):
    sidebar = portal.Sidebar(page)
    full_name = sidebar.full_name.inner_text().strip()
    first_name, last_name = '', ''
    if full_name:
        names = full_name.split(' ')
        first_name = names[0]
        if len(names) == 1:
            last_name = ''
        else:
            last_name = names[-1]

    # _set_names(profile)

    percentage_text = sidebar.completeness_percent.inner_text()
    completeness_percentage = ''.join(filter(str.isdigit, percentage_text))

    percent_text = sidebar.percent_value.inner_text()
    percentage_value = ''.join(filter(str.isdigit, percent_text))

    av_connects = sidebar.available_connects.inner_text()
    available_connects = ''.join(filter(str.isdigit, av_connects))

    categories = sidebar.categories.inner_text().split('\n')

    jobs = portal.Job(page)
    print(jobs.count)
    rc_jobs: list[md.RecommendedJobs] = []
    for i in range(0, jobs.count):
        jobs.index(i)
        rj = md.RecommendedJobs(
            title=jobs.title.inner_text(),
            featured=jobs.featured.is_visible(),
            payment_verified=jobs.payment_verified.is_visible(),
            age=jobs.age.inner_text(),
            proposals=jobs.proposals.inner_text(),
            client_country=jobs.client_country.inner_text(),
            project=md.Project(
                type_=jobs.type_.inner_text(),
                description=html.unescape(jobs.description.inner_text()),
                level=jobs.level.inner_text(),
            )
        )

        if 'hourly' not in rj.project.type_.lower():
            
            s_value = jobs.est_budget.inner_text().strip()

            rj.project.est_budget = float(''.join(filter(str.isdigit, s_value)))
            
        else:
            type_budget = jobs.type_.inner_text()
            rj.project.type_ = type_budget.split(':')[0]

            value_range = type_budget.split(':')[1].strip()
            value_range = value_range.split('-')
            min, max = [float(''.join(filter(str.isdigit, v))[:-2])
                        for v in value_range]

            rj.project.est_budget = md.EstBudget(min=min, max=max)

            rj.project.est_duration = jobs.est_duration.inner_text()
        rc_jobs.append(rj)

    profile = md.Profile(
        first_name=first_name,
        last_name=last_name,
        full_name=sidebar.full_name.inner_text().strip(),
        title=sidebar.title.inner_text(),
        completeness_percentage=completeness_percentage,
        pendencies=md.Pendencies(
            suggested_action=sidebar.suggested_action.inner_text(),
            percentage_value=percentage_value
        ),
        available_connects=available_connects,
        visibility=sidebar.visibility.inner_text(),
        availability=sidebar.availability.inner_text(),
        categories=categories,
        recommended_jobs=rc_jobs
    )

    os.makedirs('output', exist_ok=True)
    with open(f'output/{profile.first_name}_profile.json', 'w', encoding='utf8') as f:
        f.write(profile.json())
    
        


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
        login.authenticate(page)
        scan_main_page(page)
        page.pause()


if __name__ == '__main__':
    main()

## login error handler => Message: "Due to technical difficulties we are unable to process your request. Please try again later.""

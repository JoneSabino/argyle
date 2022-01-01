from playwright.sync_api import Page, Locator


class Sidebar:
    def __init__(self, page: Page):
        self.page = page

    @property
    def full_name(self) -> Locator:
        return self.page.locator(':nth-match(div.account-name, 1)')

    @property
    def title(self) -> Locator:
        return self.page.locator('p.mt-5')

    @property
    def completeness_percent(self) -> Locator:
        return self.page.locator('span.up-progress-label')

    @property
    def suggested_action(self) -> Locator:
        return self.page.locator('a.up-btn-link span:nth-child(2)')

    @property
    def percent_value(self) -> Locator:
        return self.page.locator('a.up-btn-link span:nth-child(3)')

    @property
    def available_connects(self) -> Locator:
        return self.page.locator('a[href$="membership/index"]')

    @property
    def visibility(self) -> Locator:
        return self.page.locator('span.pt-5')

    @property
    def availability(self) -> Locator:
        return self.page.locator('div.pb-20 > span > span')

    @property
    def categories(self) -> Locator:
        return self.page.locator('section[data-test="sidebar-categories"] > div:last-child')


class Job:
    def __init__(self, page: Page):
        self.cards = page.locator(
            'div[data-test="job-tile-list"] > section')
        # inside this matches, each <section> is one recommended job
        self.count = self.cards.count()

    def index(self, i: int):
        self.i = i

    @property    
    def matches(self) -> Locator:  
        return  self.cards.nth(self.i)

    @property
    def title(self) -> Locator:
        return self.matches.locator('h4.job-tile-title > a')

    @property
    def job_digest(self) -> Locator:
        '''Little line below the job title with brief info about the project
        '''
        return self.matches.locator('small.display-inline-block')

    @property
    def type_(self) -> Locator:
        return self.job_digest.locator('strong[data-test="job-type"]')

    @property
    def level(self) -> Locator:
        return self.job_digest.locator('span[data-test="contractor-tier"]')

    @property
    def est_budget(self) -> Locator:
        return self.job_digest.locator('span[data-test="budget"]')

    @property
    def est_duration(self) -> Locator:
        return self.job_digest.locator('span[data-test="duration"]')

    @property
    def age(self) -> Locator:
        return self.job_digest.locator('span[data-test="posted-on"] > span')

    @property
    def featured(self) -> Locator:
        return self.matches.locator('span.badge-featured')

    @property
    def payment_verified(self) -> Locator:
        return self.matches.locator('small[data-test="payment-verification-status"] > strong')

    @property
    def client_country(self) -> Locator:
        return self.matches.locator('small[data-test="client-country"] > strong')

    @property
    def proposals(self) -> Locator:
        return self.matches.locator('small.d-inline-block > strong[data-test="proposals"]')

    @property
    def skills_wrapper(self) -> Locator:
        '''
        each <a> element inner text inside this wrapper contains a skill
        '''
        return self.matches.locator('div.up-skill-wrapper')

    @property
    def description(self) -> Locator:
        return self.matches.locator('div.break > div > span')

from __future__ import annotations
import html
import traceback
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.retry import retry_if_exception_type
from playwright.sync_api import Page, Locator, ElementHandle, TimeoutError
import models.model as md


class Sidebar:
    '''
    Main page's sidebar elements
    '''

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
    '''
    Main page's recommended jobs panel elements
    '''

    def __init__(self, page: Page):
        # locator for all the cards available
        self.page = page

    def select_card(self, i: int):
        self.i = i

    @property
    def cards(self) -> Locator:
        return self.page.locator(
            'div[data-test="job-tile-list"] > section')

    @property
    def count(self) -> int:
        return self.cards.count()

    @property
    def matches(self) -> Locator:
        return self.cards.nth(self.i)

    @property
    def r_matches(self) -> list[ElementHandle]:
        return self.cards.element_handles()

    @property
    def job_title(self) -> Locator:
        return self.matches.locator('h4.job-tile-title > a')

    @property
    def job_digest(self) -> Locator:
        '''Little line below the job title with brief info about the project
        '''
        return self.matches.locator('small.display-inline-block')

    @property
    def job_type(self) -> Locator:
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


class Portal(Sidebar, Job):
    def __init__(self, page: Page):
        self.page = page

    def __split_name(self, full_name: str) -> tuple[str, str]:

        names = full_name.split(' ')

        first_name = names[0]
        last_name = '' if len(names) == 1 else names[-1]

        return (first_name, last_name)

    def __get_numeric_value(self, text: str) -> int:
        '''
        Extract the numbers from the string.
        '''
        try:
            return int(''.join(filter(str.isdigit, text)))
        except ValueError:
            print(traceback.format_exc())
            print('Returning the value: 0')
            return 0

    def __parse_budget_values(self, text: str) -> tuple[float, float]:
        '''
        Extracts from the text, the min and max hour rate
        for the job.
        Example:
            Input: 'Hourly: $15.00-$18.00'
            Output: (15.0, 18.0)
        '''
        try:
            value_range = text.split(':')[1].strip().split('-')
            min, max = [float(''.join(filter(str.isdigit, v))[:-2])
                        for v in value_range]
        except IndexError:
            print(traceback.format_exc())
            min, max = 0.0, 0.0
            print('Returning min and max with the value: 0.0')

        return (min, max)

    def __get_text(self, locator: Locator) -> str:
        if locator.is_enabled():
            return locator.inner_text().strip()
        else:
            return 'Field not found during scan'

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(Exception))
    def scan(self) -> md.Model:
        '''
        Scans the relevant information from the
        portal main page and structure it in a 
        pydantic model.
        '''
        try:
            p = md.Profile(pendencies=md.Pendencies())

            p.full_name = self.__get_text(self.full_name)
            p.first_name, p.last_name = self.__split_name(p.full_name)

            p.title = self.__get_text(self.title)

            p.completeness_percentage = self.__get_numeric_value(
                self.__get_text(self.completeness_percent))

            p.available_connects = self.__get_numeric_value(
                self.__get_text(self.available_connects))

            p.categories = self.__get_text(self.categories).split('\n')

            p.pendencies.suggested_action = self.__get_text(self.suggested_action)
            p.pendencies.percentage_value = self.__get_numeric_value(
                self.__get_text(self.percent_value))

            p.visibility = self.__get_text(self.visibility)
            p.availability = self.__get_text(self.availability)

            rc_jobs: list[md.RecommendedJobs] = []
            for i in range(0, self.count):
                self.select_card(i)

                rj = md.RecommendedJobs(project=md.Project())

                rj.title = self.__get_text(self.job_title)
                rj.featured = self.featured.is_visible()
                rj.project.type = self.__get_text(self.job_type)
                rj.project.level = self.__get_text(self.level)
                rj.age = self.__get_text(self.age)
                rj.project.description = html.unescape(
                    self.__get_text(self.description))
                rj.proposals = self.__get_text(self.proposals)
                rj.client_country = self.__get_text(self.client_country)
                rj.payment_verified = self.payment_verified.is_visible()

                if 'hourly' not in rj.project.type.lower():
                    eb = self.__get_text(self.est_budget)
                    rj.project.est_budget = float(self.__get_numeric_value(eb))
                else:
                    try:
                        rj.project.est_duration = self.__get_text(
                            self.est_duration)
                        type_n_budget = rj.project.type
                        rj.project.type = type_n_budget.split(':')[0]
                        min, max = self.__parse_budget_values(type_n_budget)
                        rj.project.est_budget = md.EstBudget(min=min, max=max)
                    except IndexError:
                        print(traceback.format_exc())
                        rj.project.est_budget = 0.0

                rc_jobs.append(rj)
            p.recommended_jobs = rc_jobs
            profile = md.Model(profile=p)

        except TimeoutError:
            print(traceback.format_exc())
            print("Some element couldn't be found in time.")
            profile = md.Model()
        except:
            print(traceback.format_exc())
            raise Exception('Retrying. After the 3rd tentative the execution will stop.')

        return profile

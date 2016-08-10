from __future__ import unicode_literals

import urlparse
import random

import silly
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium.webdriver.chrome.webdriver import \
    WebDriver  # TODO: make this work on firefox, too (I got stuck at finding xpath in the browser)

from communities.models import Community, Committee
from users.models import OCUser

from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

from selenium import webdriver

# import for test_publish_meeting_to_me_only
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

NUM_OF_SUPER_USERS = 1
NUM_OF_USERS = 1
DEFAULT_PASS = "secret"


class ExampleCommunityLiveTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(ExampleCommunityLiveTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        # self.selenium.get(self.full_url(reverse('logout')))
        cls.selenium.quit()
        super(ExampleCommunityLiveTests, cls).tearDownClass()

    def setUp(self):
        self.community = Community.objects.create(
            name="Kibbutz Broken Dream",
        )
        self.susers_details = dict()
        self.users_details = dict()
        for i in range(NUM_OF_SUPER_USERS):
            name = silly.name(slugify=True)
            email = silly.email()
            self.susers_details[name] = OCUser.objects.create_superuser(email, name, DEFAULT_PASS)
        for i in range(NUM_OF_USERS):
            name = silly.name(slugify=True)
            email = silly.email()
            self.users_details[name] = OCUser.objects.create_user(email, name, DEFAULT_PASS)
        self.committee = Committee.objects.create(name="Culture", slug="culture", community=self.community)

        self.u1 = OCUser.objects.create_superuser("menahem.godick@gmail.com", "Menahem", "secret")
        # self.selenium = WebDriver()
        # self.browser = webdriver.Chrome()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        print("1st")
        yield
        print("2nd")
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )
        print("3rd")

    """
    Note: compare this:
    from selenium import webdriver

    self.browser = webdriver.Firefox()
    to this:
    from selenium.webdriver.chrome.webdriver import WebDriver
    self.selenium = WebDriver()

    """

    def full_url(self, s):
        if s.startswith(self.live_server_url):
            return s
        else:
            return self.live_server_url + s

    def get_current_path(self):
        return urlparse.urlsplit(self.selenium.current_url).path

    def assert_current_path(self, path):
        self.assertEqual(self.full_url(path), self.full_url(self.get_current_path()))

    def selenium_get_and_assert(self, url):
        """
        Tries to go url (as is) and then asserts that current_path == url
        """
        self.selenium.get(url)
        self.assert_current_path(url)

    def login(self, goto_login=True, name=None, pswd=DEFAULT_PASS):
        if goto_login is True:
            self.selenium.get(self.full_url(reverse('login')))
        self.assert_current_path(reverse('login'))
        if name is None:
            name = random.choice(self.susers_details.keys())
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys(self.susers_details[name].email)
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys(pswd)
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

    def test_redirect_and_login(self):
        print("{} start".format("test_redirect_and_login"))
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        self.login(
            goto_login=False)  # False since the community we created is private - it should automatically redircet to login
        print("{} end".format("test_redirect_and_login"))


    #Use Menahems' test_publish_meeting_to_me_only
    """
    TODO:
    Make sure the DB has:
    Community, Committee...


     Afer resending check in db that Committee.upcoming_meeting_version is up by 1


    :return:
    """

    def test_resend_agenda(self):
        self.login()
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)

        # from IPython import embed
        # embed()
        # Navigate to committee page.
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()
        # embed()
        # self.selenium.find_element_by_xpath('//a[@href="{}main/upcoming/edit/"]'.format(
        #     self.community.get_absolute_url())).click()
        #
        # title = WebDriverWait(self.selenium, 10).until(
        #     ec.presence_of_element_located((By.ID, "id_upcoming_meeting_title"))
        # )
        # title.send_keys("Meeting Title")
        # self.selenium.find_element_by_id("id_upcoming_meeting_location").send_keys("Tel Aviv")
        # self.selenium.find_element_by_id("id_upcoming_meeting_scheduled_at_0").send_keys("01/01/2017")
        # self.selenium.find_element_by_id("id_upcoming_meeting_scheduled_at_1").send_keys("02:00PM", Keys.TAB)
        # current_element = self.selenium.switch_to.active_element
        # current_element.send_keys("Background...")
        # self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        #
        # # Test: If there is a h1 title "Meeting Title", Its OK.
        # time.sleep(0.6)
        # self.assertTrue(self.is_element_present(By.XPATH, "//* [contains(text(), 'Meeting Title')]"))
        #
        # # Add a quick issue to the meeting
        # self.selenium.find_element_by_xpath(
        #     '//input[@type="text"]').send_keys("Building a new road")
        # self.selenium.find_element_by_xpath('//button[@id="quick-issue-add"]').click()
        #
        # # Test: If there is at least one element of 'Issue' in line, Its OK.
        # time.sleep(0.2)
        # agenda_lines = self.selenium.find_elements_by_xpath('//ul[@id="agenda"]')
        # self.assertTrue(len(agenda_lines) > 0)
        #
        # # Add a quick proposal to the issue
        # button = WebDriverWait(self.selenium, 10).until(
        #     ec.presence_of_element_located((
        #         By.LINK_TEXT, 'Building a new road')))
        # button.click()
        # # self.selenium.find_element_by_link_text("Building a new road").click()
        # self.selenium.find_element_by_id("quick-proposal-title").send_keys("New Proposal")
        # self.selenium.find_element_by_id("quick-proposal-add").click()
        #
        # # Test: If there is a line with text "New Proposal", Its OK.
        # time.sleep(0.6)
        # self.assertTrue(self.is_element_present(By.XPATH, "//* [contains(text(), 'New Proposal')]"))
        #
        # # Navigate to committee page.
        # self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
        #     self.community.get_absolute_url())
        # ).click()
        #
        # # Click on publish button.
        # self.selenium.find_element_by_xpath('//a[@href="{}main/upcoming/publish/"]'.format(
        #     self.community.get_absolute_url())).click()
        #
        # # Select "only me" option in popup form.
        # form_select_me = WebDriverWait(self.selenium, 10).until(
        #     ec.presence_of_element_located((By.ID, "id_me"))
        # )
        # form_select_me.send_keys(Keys.SPACE)
        #
        # # Click on publish button in popup form.
        # self.selenium.find_element_by_css_selector('input[type="submit"][value="Publish"]').click()
        #
        # # Test: If there is a li class = "info", Its OK.
        # time.sleep(1)
        # self.assertTrue(self.is_element_present(
        #     By.CLASS_NAME, "info"))







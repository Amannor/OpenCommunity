from __future__ import unicode_literals

import time
import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from communities.models import Community
from users.models import OCUser

class ExampleCommunityLiveTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(ExampleCommunityLiveTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ExampleCommunityLiveTests, cls).tearDownClass()

    def login(self, user):
        login_url = self.full_url(reverse("login"))
        self.selenium.get(login_url)

        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys(user.email)
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys("secret")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

    def setUp(self):
        self.community = Community.objects.create(
            name="Kibbutz Broken Dream",
        )
        self.u1 = OCUser.objects.create_superuser("menahem.godick@gmail.com", "Menahem", "secret")

    def full_url(self, s):
        return self.live_server_url + s

    def get_current_path(self):
        return urlparse.urlsplit(self.selenium.current_url).path

    def assert_current_path(self, path):
        self.assertEqual(path, self.get_current_path())

    def is_element_present(self, how, what):
        try:
            self.selenium.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def get_committees_upcoming_meeting_versions(self):
        upcoming_meeting_versions = list()
        for committee in self.community.get_committees():
            upcoming_meeting_versions.append(committee.upcoming_meeting_version)
        return upcoming_meeting_versions

    def publish_to_recipients(self, recipients_ids):
        # Click on publish button.
        self.selenium.find_element_by_xpath('//a[@href="{}main/upcoming/publish/"]'.format(
            self.community.get_absolute_url())).click()
        for id in recipients_ids:
            form_select_me = WebDriverWait(self.selenium, 10).until(
                ec.presence_of_element_located((By.ID, id))
            )
        form_select_me.send_keys(Keys.SPACE)
        # Click on publish button in popup form.
        self.selenium.find_element_by_css_selector('input[type="submit"][value="Publish"]').click()

    def test_redirect_login(self):
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        # time.sleep(2)

        # Test: If there is 'login' in the URL, its OK.
        self.assert_current_path(reverse('login'))
        # self.login(self.u1)

    def test_community_is_open_for_superuser(self):
        # login by superuser
        self.login(self.u1)
        # Try enter to community page
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        # If the status code is 200 its OK.
        # r = requests.get(url)
        # self.assertEquals(r.status_code, 200)

        # Test: If the link element 'Committee' is exist, Its OK.
        # time.sleep(0.2)
        self.assertTrue(self.is_element_present(By.XPATH, '//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())))

    def test_logout(self):
        # login for trying logout
        self.login(self.u1)

        # Flow of all clicking to logout
        self.selenium.find_element_by_class_name('dropdown-toggle').click()
        self.selenium.find_element_by_xpath('//a[@href="/logout/"]').click()

        # Try to enter to community page after logout.
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)

        # Test: If now its redirect to login page, that's OK.
        self.assert_current_path(reverse('login'))

    def test_create_quick_new_issue_for_new_meeting(self):
        self.login(self.u1)
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()
        self.selenium.find_element_by_xpath(
            '//input[@type="text"]').send_keys("Building a new road")
        self.selenium.find_element_by_xpath('//button[@id="quick-issue-add"]').click()

        # Test: If there is at least one element of 'Issue' in line, Its OK.
        time.sleep(0.2)
        agenda_lines = self.selenium.find_elements_by_xpath('//ul[@id="agenda"]')
        self.assertTrue(len(agenda_lines) > 0)

    def test_create_lazy_new_issue_for_new_meeting(self):
        self.login(self.u1)
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()
        self.selenium.find_element_by_xpath('//a[@href="{}main/issues/upcoming-create/"]'.format(
            self.community.get_absolute_url())
        ).click()

        title = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.ID, "id_title"))
        )
        title.send_keys("Building a new road", Keys.TAB)
        current_element = self.selenium.switch_to.active_element
        current_element.send_keys("The Kibutz needs a new access road from the other side..")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # Test: If there is at least one element of 'Issue' in line, Its OK.
        time.sleep(0.5)
        agenda_lines = self.selenium.find_elements_by_xpath('//ul[@id="agenda"]')
        self.assertTrue(len(agenda_lines) > 0)

    def test_create_new_restricted_issue_for_new_meeting(self):
        self.login(self.u1)
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()
        self.selenium.find_element_by_xpath('//a[@href="{}main/issues/upcoming-create/"]'.format(
            self.community.get_absolute_url())
        ).click()

        # Choose to be restricted issue by clicking on reason 2.
        restricted_toggle = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'issue-btn-confidential'))
        )
        restricted_toggle.send_keys(Keys.ENTER)
        self.selenium.find_element_by_xpath('//label[@for="id_confidential_reason_2"]').click()

        # Filling up all the fields just to be sure everything is ok.
        self.selenium.find_element_by_id("id_title").send_keys("Restricted issue", Keys.TAB)
        current_element = self.selenium.switch_to.active_element
        current_element.send_keys("Restricted issue for example..")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # Test: If there is a link text "Restricted issue", Its OK.
        time.sleep(0.6)
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Restricted issue"))
        # self.assertTrue(self.is_element_present(By.XPATH, "//*[contains(text(), 'Restricted issue')]"))

    def test_start_new_quick_meeting(self):
        self.login(self.u1)
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()

        # Click on button of "Start Meeting"
        self.selenium.find_element_by_xpath('//button[@data-url="{}main/upcoming/start/"]'.format(
            self.community.get_absolute_url())).click()

        # Click on "Start Meeting" button.
        restricted_toggle = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.XPATH, '//input[@type="submit"]'))
        )
        restricted_toggle.click()

        # Test: If the link element 'Stop Meeting' is exist, Its OK.
        time.sleep(0.3)
        self.assertTrue(self.is_element_present(By.CLASS_NAME, "fa"))

    def test_create_quick_new_proposal_for_issue(self):
        self.login(self.u1)
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()

        # Add a quick issue to the meeting
        self.selenium.find_element_by_xpath(
            '//input[@type="text"]').send_keys("Building a new road")
        self.selenium.find_element_by_xpath('//button[@id="quick-issue-add"]').click()

        # Add a quick proposal to the issue
        button = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((
                By.LINK_TEXT, 'Building a new road')))
        button.click()
        # self.selenium.find_element_by_link_text("Building a new road").click()
        self.selenium.find_element_by_id("quick-proposal-title").send_keys("New Proposal")
        self.selenium.find_element_by_id("quick-proposal-add").click()

        # Test: If there is a line with text "New Proposal", Its OK.
        time.sleep(0.6)
        self.assertTrue(self.is_element_present(By.XPATH, "//* [contains(text(), 'New Proposal')]"))

    def test_create_new_draft_meeting(self):
        self.login(self.u1)
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()

        self.selenium.find_element_by_xpath('//a[@href="{}main/upcoming/edit/"]'.format(
            self.community.get_absolute_url())).click()

        title = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.ID, "id_upcoming_meeting_title"))
        )
        title.send_keys("Meeting Title")
        self.selenium.find_element_by_id("id_upcoming_meeting_location").send_keys("Tel Aviv")
        self.selenium.find_element_by_id("id_upcoming_meeting_scheduled_at_0").send_keys("01/01/2017")
        self.selenium.find_element_by_id("id_upcoming_meeting_scheduled_at_1").send_keys("02:00PM", Keys.TAB)
        current_element = self.selenium.switch_to.active_element
        current_element.send_keys("Background...")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # Test: If there is a h1 title "Meeting Title", Its OK.
        time.sleep(0.6)
        self.assertTrue(self.is_element_present(By.XPATH, "//* [contains(text(), 'Meeting Title')]"))

    def test_publish_meeting_to_me_only(self):
        mail_recipients_ids = list()
        mail_recipients_ids.append("id_me")

        self.login(self.u1)
        url = self.full_url(self.community.get_absolute_url())
        self.selenium.get(url)

        # Navigate to committee page.
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()

        self.selenium.find_element_by_xpath('//a[@href="{}main/upcoming/edit/"]'.format(
            self.community.get_absolute_url())).click()

        title = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.ID, "id_upcoming_meeting_title"))
        )
        title.send_keys("Meeting Title")
        self.selenium.find_element_by_id("id_upcoming_meeting_location").send_keys("Tel Aviv")
        self.selenium.find_element_by_id("id_upcoming_meeting_scheduled_at_0").send_keys("01/01/2017")
        self.selenium.find_element_by_id("id_upcoming_meeting_scheduled_at_1").send_keys("02:00PM", Keys.TAB)
        current_element = self.selenium.switch_to.active_element
        current_element.send_keys("Background...")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # Test: If there is a h1 title "Meeting Title", Its OK.
        time.sleep(0.6)
        self.assertTrue(self.is_element_present(By.XPATH, "//* [contains(text(), 'Meeting Title')]"))

        # Add a quick issue to the meeting
        self.selenium.find_element_by_xpath(
            '//input[@type="text"]').send_keys("Building a new road")
        self.selenium.find_element_by_xpath('//button[@id="quick-issue-add"]').click()

        # Test: If there is at least one element of 'Issue' in line, Its OK.
        time.sleep(0.2)
        agenda_lines = self.selenium.find_elements_by_xpath('//ul[@id="agenda"]')
        self.assertTrue(len(agenda_lines) > 0)

        # Add a quick proposal to the issue
        button = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((
                By.LINK_TEXT, 'Building a new road')))
        button.click()
        # self.selenium.find_element_by_link_text("Building a new road").click()
        self.selenium.find_element_by_id("quick-proposal-title").send_keys("New Proposal")
        self.selenium.find_element_by_id("quick-proposal-add").click()

        # Test: If there is a line with text "New Proposal", Its OK.
        time.sleep(0.6)
        self.assertTrue(self.is_element_present(By.XPATH, "//* [contains(text(), 'New Proposal')]"))

        # Navigate to committee page.
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()

        self.publish_to_recipients(mail_recipients_ids)

        # Test: If there is a li class = "info", Its OK.
        time.sleep(1)
        self.assertTrue(self.is_element_present(
            By.CLASS_NAME, "info"))

    def test_resend_agenda(self):
        mail_recipients_ids = list()
        mail_recipients_ids.append("id_send_to_1")
        self.test_publish_meeting_to_me_only()
        old_meeting_versions = self.get_committees_upcoming_meeting_versions()
        self.publish_to_recipients(mail_recipients_ids)
        version_incremented_properly = False
        time.sleep(0.1)
        # Currently checking all versions - we only need one to increment for the test to pass
        for committee in self.community.get_committees():
            for version in old_meeting_versions:
                if version == committee.upcoming_meeting_version - 1:
                    version_incremented_properly = True
                    break;
            if version_incremented_properly:
                break
        self.assertTrue(version_incremented_properly, "Version didn't increment properly")

    def test_edit_issue_after_agenda_sent(self):
        edit_addition_text = "_addendum"
        mail_recipients_ids = list()
        mail_recipients_ids.append("id_me")
        self.test_publish_meeting_to_me_only()
        issue = self.selenium.find_element_by_xpath('//*[@id="agenda"]/li/a')
        issue.click()
        subject = self.selenium.find_element_by_xpath('// *[ @ id = "issue-detail"] / div[1] / div[1] / div / div / div[2] / div[2] / div / div[3] / div / div[1] / \
                                               div[1] / div[1] / h5 / a[1]')
        subject.click()
        title = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.ID, "id_title"))
        )
        old_title_value = title.get_attribute('value')
        title.send_keys(edit_addition_text)
        # Save
        self.selenium.find_element_by_id("issue_edit_submit").click()

        # assert title edit worked properly
        time.sleep(0.4)
        new_title = self.selenium.find_element_by_xpath(
            '//*[@id="issue-detail"]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[1]/h1').text
        self.assertEqual(new_title, "{}{}".format(old_title_value, edit_addition_text))

        # Go back to meeting and (Re)Publish the agenda
        self.selenium.find_element_by_xpath('//*[@id="issue-detail"]/div[1]/div[1]/div/div/div[1]/a').click()
        self.publish_to_recipients(mail_recipients_ids)

    def test_add_proposal_after_agenda_sent(self):
        mail_recipients_ids = list()
        mail_recipients_ids.append("id_me")
        self.test_publish_meeting_to_me_only()

        # Navigate to first issue page.
        self.selenium.find_element_by_xpath('//a[@href="{}main/issues/1/"]'.format(
            self.community.get_absolute_url())
        ).click()

        # input additional proposal text
        new_proposal_title = WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.ID, "quick-proposal-title"))
        )
        new_proposal_title.send_keys(
            "My brand new proposal")  # TODO - add static counter so as to add different proposal titles
        # Press the 'Add' btn
        self.selenium.find_element_by_id('quick-proposal-add').click()
        # Go back to meeting page & (re)publish agenda
        time.sleep(0.5)
        self.selenium.find_element_by_xpath('//a[@href="{}main/"]'.format(
            self.community.get_absolute_url())
        ).click()
        self.publish_to_recipients(mail_recipients_ids)

    def test_vote_on_proposal(self):
        pass

    def generic_proposal_action(self, issue_num=1, accept_proposal=True):
        self.test_publish_meeting_to_me_only()
        # Start meeting
        self.selenium.find_element_by_class_name('btn-default').click()
        WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="modal-form"]/div/form/div/div[3]/input'))).click()

        # Goto n-th issue -> 1st proposal
        time.sleep(1)
        self.selenium.find_element_by_xpath('//a[@href="{}main/issues/{}/"]'.format(
            self.community.get_absolute_url(), issue_num)
        ).click()
        WebDriverWait(self.selenium, 10).until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, 'check_box'))).click()  # Will choose 1st proposal (consider making it dynamic)

        # Accept \ reject
        wanted_btn_num = 1 if accept_proposal else 2
        btn_generic_xpath = '// *[ @ id = "proposal-form"] / div / button[{}]'
        self.selenium.find_element_by_xpath(btn_generic_xpath.format(wanted_btn_num)).click()

        """
        Check if if we accepted \ rejected properly
        Note - currently only checking that exactly one btn is left present
        (TODO: If we accepted, check that only the reject btn is present, and vice versa)
        """
        self.assertEqual(len(self.selenium.find_elements_by_xpath(btn_generic_xpath.format(1))), 1)
        self.assertEqual(len(self.selenium.find_elements_by_xpath(btn_generic_xpath.format(2))), 0)

    def test_accept_proposal(self):
        self.generic_proposal_action()

    def test_reject_proposal(self):
        self.generic_proposal_action(accept_proposal=False)

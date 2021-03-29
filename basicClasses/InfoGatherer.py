"""
    Copyright 2021 Kejie He 何克杰

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# -*- encoding:utf-8 -*-
# Dependencies
import os
import sys
import time
from collections import namedtuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

Locator = namedtuple('Locator', ['by', 'value'])

sys.path.append(os.getcwd())


def chromedriver_init():
    """
    This function returns a headless incognito chromedriver
    :return: chromedriver
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--incognito")
    try:
        browser = webdriver.Chrome(options=chrome_options)
    except WebDriverException:
        browser = webdriver.Chrome(options=chrome_options,executable_path="../chromedriver.exe")
    browser.maximize_window()
    return browser


def course_list_parser(courses):
    """
    This function takes in a list of courses and parse it into SkillTreeNode shortName standard
    :param courses: a list of string, each represent a course
    :return: a list of shortnames
    """
    parsed = []
    for course in courses:
        course = str(course)
        if len(course) != 0:
            parsed.append("-".join(course.split(" ")).upper())
    return parsed


class InfoGatherer:
    """
    This class takes your SIS account name and psw to gather your account information
    """

    def __init__(self, username, password):
        """
        Initializes the InfoGatherer
        :param username: your SIS username
        :param password: your SIS password
        """
        # Record the username and password
        self.driver = chromedriver_init()
        self.url = "http://sis.rpi.edu"
        self.username = username
        self.password = password
        # Initialize and stay in the login stage
        self.__go_until_login_page_loaded()
        if self.__try_to_login():
            print("Log in successful")
            self.logged_in = True
        else:
            print("Log in failure, username&password combination incorrect")
            self.logged_in = False

    def __goto_page(self):
        """
        Goto the self.url page
        :return: None
        """
        self.driver.get(self.url)

    def __wait_element(self, element_path, time_limit=30):
        """
        Wait for element to load
        :param element_path: XPATH of the element
        :param time_limit: default to 30s, can customize
        :return: True if element load in time limit, False otherwise
        """
        try:
            WebDriverWait(self.driver, time_limit).until(
                EC.element_to_be_clickable(locator=Locator(by=By.XPATH, value=element_path))
            )
            # print("Element found!")
            return True
        except TimeoutException:
            print("Cannot find the given element in {} time limit, returning false".format(time_limit))
            print("XPATH given: {}".format(element_path))
            return False

    def __click(self, element_path):
        """
        Find the element then click
        :param element_path: XPATH of the element
        :return: None
        """
        if self.__wait_element(element_path):
            self.driver.find_element_by_xpath(element_path).click()

    def __text_input(self, element_path, text_input):
        """
        Input the given text into the element
        :param element_path: XPATH of the element
        :param text_input: the actual text to be inputted
        :return:
        """
        if self.__wait_element(element_path):
            element = self.driver.find_element_by_xpath(element_path)
            element.click()
            element.send_keys(str(text_input))

    # def go_until_element_found(self, element_path):
    #     """
    #     Load the url, found the given element
    #     XPATH of loading box: '//*[@id="login"]'
    #     :param element_path: XPATH of the element to be found
    #     :return: None
    #     """
    #     self.goto_page()
    #     self.wait_element(element_path)

    def __go_until_login_page_loaded(self):
        """
        Load the SIS page, wait until it completes loading
        :return: None
        """
        self.__goto_page()
        self.__wait_element('//*[@id="login"]')

    def __try_to_login(self):
        """
        This sequence tries to load the SIS main system, will print error message on failure
        :return: True if the page successfully log into the SIS main page, False otherwise
        """
        self.__text_input('//*[@id="username"]', self.username)
        # time.sleep(1)
        self.__text_input('//*[@id="password"]', self.password)
        # time.sleep(1)
        self.__click('//*[@id="password"]/../../..//input[@name="submit"]')
        # time.sleep(1)
        return self.__wait_element('//div[@class="headerlinksdiv"]//table[@class="plaintable"]//table//td[3]',
                                   time_limit=10)

    def __try_to_fetch_learned_courses(self):
        """
        This function tries to fetch learned courses
        :return: The learned courses in a string
        """
        self.__click('//div[@class="headerlinksdiv"]//table[@class="plaintable"]//table//td[3]')
        # time.sleep(1)
        self.__click('//table[@class="menuplaintable"]//td[contains(.,"Degree Works")]/a')
        # time.sleep(1)
        self.__click('//button[@title="More"]')
        # time.sleep(1)
        self.__click('//li[contains(.,"Class History")]')
        # time.sleep(1)

        # Try to read out the course name and print
        if self.__wait_element('//div[@role="dialog"]//*[@id="TermDivider"]/..//div//tr/td[1]'):
            course_list = self.driver.find_elements_by_xpath(
                '//div[@role="dialog"]//*[@id="TermDivider"]/..//div//tr/td[1]')
            course_str = [ele.text for ele in course_list if len(ele.text) > 0]

            # print(course_str)
            return course_str
        else:
            raise Exception("Failed to enter the degreework page")

    def quit(self):
        """
        This function quits the chromedriver, recommanded at the end of the usage
        :return: None
        """
        self.driver.quit()

    def get_learned_courses(self):
        """
        Get the learned courses of the SIS user provided in initialization
        :return: A list of learned courses
        """
        self.__goto_page()
        self.__wait_element('//div[@class="headerlinksdiv"]//table[@class="plaintable"]//table//td[3]')
        return course_list_parser(self.__try_to_fetch_learned_courses())

    def add_course_from_SIS(self):
        print("Simulating adding course from SIS, to be implemented")
        pass


if __name__ == "__main__":
    Gatherer = InfoGatherer(input("Enter your SIS username: "), input("Enter your sis password: "))
    if Gatherer.logged_in:
        print(Gatherer.get_learned_courses())
    Gatherer.quit()
    time.sleep(5)

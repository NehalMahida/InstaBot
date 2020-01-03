from telnetlib import EC

from selenium import webdriver
import os
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class IgBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'
        # you need to download chrome driver according to your chrome browser version.
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.login()

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        time.sleep(4)
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        time.sleep(4)

    def unfollower(self, account):
        # account has the value of username.
        self.driver.get("https://www.instagram.com/{0}/".format(account))
        # 2 second break for loading of homepage.
        time.sleep(2)
        self.driver.find_element_by_partial_link_text("following").click()
        # 4 second break for loading of following panel.
        time.sleep(4)
        # dialog is the xpath of the scrolling window of the following panel.
        dialog = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        # This path is for the pop-window open for confirmation for unfollow.
        path = "/html/body/div[5]/div/div/div[3]/button[1]"
        i = 1
        while i < 25:
            try:
                # This xpath is for the button available to unfollow the user.
                xpath = "/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]/button".format(i)
                self.driver.find_elements_by_xpath(xpath)[0].click()
                time.sleep(1)
                self.driver.find_elements_by_xpath(path)[0].click()
                time.sleep(2)
                i += 1
            except IndexError:
                print('ex')
                time.sleep(1)
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", dialog
                )

    def nav_user(self, user):
        self.driver.get('{}/{}'.format(self.base_url, user))

    def follow_user(self, user):
        # user has username.
        # This will redirect page towards the user profile (having lots of followers to follow!)
        self.driver.get('{}/{}'.format(self.base_url, user))
        # self.nav_user(user)
        self.driver.find_element_by_partial_link_text("followers").click()
        time.sleep(4)
        dialog = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        j = 1
        i = 1
        while i < 26:
            # Try except is for if the xpath is not available exception will generate and at except part
            # page will be scrolled down so that index can be generated.
            try:
                # This xpath is for the button available to follow the user.
                xpath = "/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]/button".format(j)
                str = self.driver.find_elements_by_xpath(xpath)[0]
                # print(str.text, j, i)
                # If the button has follow text then follow otherwise ignored. (ec. Following, Requested)
                if str.text == 'Follow':
                    i += 1
                    str.click()
                    time.sleep(2)
                time.sleep(1)
                j += 1
            except IndexError:
                # print('ex')
                time.sleep(1)
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", dialog
                )

    def unfollow_user(self, user):
        self.nav_user(user)
        unfollow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Following')]")[0].click()
        unfollow = self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[3]/button[1]")[0].click()


if __name__ == '__main__':
    ig_bot = IgBot('username', 'password')
    # ig_bot.unfollower('the.programeme')
    # for i in range(3):
    ig_bot.follow_user('meme_coding')


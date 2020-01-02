from telnetlib import EC

from selenium import webdriver
import os
import time

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
        self.driver.get("https://www.instagram.com/{0}/".format(account))
        time.sleep(2)
        self.driver.find_element_by_partial_link_text("following").click()
        time.sleep(4)
        dialog = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        for i in range(5):
            self.driver.execute_script("arguments[0].scrollTop = (arguments[0].scrollHeight/5)", dialog)
            time.sleep(1)
        path = "/html/body/div[5]/div/div/div[3]/button[1]"  # to click unfollow in pop-up window.
        for i in range(1, 11):
            xpath = "/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]/button".format(i)
            self.driver.find_elements_by_xpath(xpath)[0].click()
            self.driver.find_elements_by_xpath(path)[0].click()
            time.sleep(2)

    def nav_user(self, user):
        self.driver.get('{}/{}'.format(self.base_url, user))

    def follow_user(self, user):
        self.nav_user(user)
        self.driver.find_element_by_partial_link_text("followers").click()
        time.sleep(4)
        dialog = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        # Required : A good logic to scroll down.
        for k in range(10):
            self.driver.execute_script("arguments[0].scrollTop = (arguments[0].scrollHeight/10)", dialog)
            time.sleep(1)
        #
        i = 0
        j = 27
        while i < 20:
            xpath = '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]'.format(j)
            str = self.driver.find_elements_by_xpath(xpath)[0]
            print(str.text, j, i)
            if str.text == 'Follow':
                i += 1
                str.click()
                time.sleep(2)
            time.sleep(1)
            j += 1

    def unfollow_user(self, user):
        self.nav_user(user)
        unfollow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Following')]")[0].click()
        unfollow = self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[3]/button[1]")[0].click()


if __name__ == '__main__':
    ig_bot = IgBot('username', 'password')
    # ig_bot.unfollower('the.programeme')
    for i in range(3):
        ig_bot.follow_user('meme_coding')


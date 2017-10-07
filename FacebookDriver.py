from selenium import webdriver # For webpage crawling
from time import sleep
import time
from selenium.webdriver.common.keys import Keys # For input processing
from random import randint
import sys # For file path processing
import datetime # For timestamp
import pickle # For data management
import os
from xvfbwrapper import Xvfb
from Mailer import Mailer
import matplotlib.pyplot as plt

# Available comments: the first {} is replaced with the username
# the second is replaced with a smiley. Note that UTF-8 smileys are only
# supported by Firefox driver which may corrupt some timed functionalities.
class Tell:
    comment = [ "Nice {}","cool {} ","Great style {}","Amazing {}",\
                "Awesome {}","Fantastic {}","{}","Brilliant one {}",\
                "Pretty nice {}","Awesome feed {}","I like your feed {}",\
                "Top {}", "Really cool works {}", "Rad!!! {}",\
                "This is cool {}", "Love this {}", "Great {}", "Yeah {}"]
    smiley = [  ":)",":D","=D","=)",";)",":)",":)",";D" ]

class Driver(object):
    def __init__(self):
        # Set up Telegram Message Client
        self.mailer = Mailer()
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')
        self.mailer.sendMessage("Initializing FacebookDriver.")

        Set up virtual display for Raspberry Pi compatibility
        self.display = Xvfb()
        self.display.start()

        # The following (xpath) classes need to be refreshed every now and then.
        # they define, where elements are located on Facebook.

        # Logging in
        self.loginXpath = "//input[@id='email']"
        self.passwordXpath = "//input[@id='pass']"
        # Elements on the hashtag page
        self.containerXpath = "//div[contains(@class, '_1dwg _1w_m')]"
        self.userNameSubXpath = "//span[contains(@class, 'fwb fcg')]"
        # Alias selection
        self.menuSubXpath = "//div[contains(@class, '_8g2')]"
        self.aliasSelectionSubXpath = ".//a[contains(@class, '_55pi _2agf _4o_4 _4jy0 _4jy3 _517h _51sy _59pe _42ft')]"
        self.companySelectionSubXpath = "//div[contains(@class, '_5ghu _alf')]"
        self.alldaycreativeSelectionSubXpath = "//div[contains(@class, ' _5dsl _alf clearfix')]"
        # Commenting
        self.commentButtonSubXpath = "//a[contains(@class, 'comment_link _5yxe')]"
        self.commentInputSubXpath = "//div[contains(@class, '_1p1v')]"
        # Liking
        self.likeButtonSubXpath = "//a[@class='UFILikeLink _4x9- _4x9_ _48-k']"
        self.likeButtonClickedSubXpath = "//a[contains(@class, 'UFILikeLink _4x9- _4x9_ _48-k UFILinkBright')]"


        self.login = input("E-Mail: ")
        self.password = input("Password: ")

        # Clearing the command line
        os.system('clear')

        # Final setup
        self.topics = ["render","cartoon","daily","art","design","cinema4d","animation","cg","illustration"]
        self.delay = 30
        self.startUrl = "https://www.facebook.com/login.php"
        self.hashtagPage = "https://www.facebook.com/hashtag/{}"

        # chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.default_content_setting_values.notifications" : 2}
        # chrome_options.add_experimental_option("prefs",prefs)
        # self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1920,1080)
        self.log = []

    def focus(self,element):
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')

        # print("Focusing element on position: ("+str(element.location["x"])+","+str(element.location["y"])+")")
        self.browser.execute_script("arguments[0].focus();", element)

    def loginToFacebook(self):
        self.mailer.sendMessage("Logging in to facebook.")
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')

        print("Logging in to facebook")
        self.browser.get(self.startUrl)
        sleep(3)
        loginField = self.browser.find_element_by_xpath(self.loginXpath)
        loginField.send_keys(self.login)
        passField = self.browser.find_element_by_xpath(self.passwordXpath)
        passField.send_keys(self.password)
        passField.send_keys(Keys.RETURN)
        sleep(10)
        return

    def getPostsFromHashtagPage(self,topic):
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')

        print("Getting posts from hashtag: #"+topic)
        self.browser.get(self.hashtagPage.format(topic))
        sleep(5)
        for scrollDownAmount in range(20):
            if self.mailer.getCurrentMessage() == "Stop":
                raise Exception('Stopped by telegram.')

            self.mailer.sendMessage("Getting posts from hashtag page. ("+str(scrollDownAmount)+"/20)")
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
        return self.browser.find_elements_by_xpath(self.containerXpath)

    def sendStats(self):
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(self.log)
        save = "likelog/log.png"
        fig.savefig(save)
        self.mailer.send_image(save)

    def selectAlldaycreative(self,menu):
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')

        self.focus(menu)
        menu.click()
        sleep(3)

        selection = menu.find_element_by_xpath(self.companySelectionSubXpath)
        selection.click()
        sleep(3)

        selections = menu.find_elements_by_xpath(self.alldaycreativeSelectionSubXpath)
        selection = selections[1]
        selection.click()
        sleep(3)

        return True

    def likeEverything(self):
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')
        self.mailer.sendMessage("Liking everything on the hashtag page.")

        print("Liking everything on the hashtag page.")
        selections = self.browser.find_elements_by_xpath(self.likeButtonSubXpath)
        self.log.append(len(selections))
        totalSelections = len(selections)
        currentSelection = 1
        for selection in selections:
            self.mailer.sendMessage("Liking post: ("+str(currentSelection)+"/"+str(totalSelections)+")")
            self.focus(selection)
            selection.click()
            currentSelection += 1
            sleep(5)

    # def commentEverything(self):
    #     if self.mailer.getCurrentMessage() == "Stop":
    #         raise Exception('Stopped by telegram.')
    #
    #     print("Commenting everything on the hashtag page.")
    #     selections = self.browser.find_elements_by_xpath(self.commentButtonSubXpath)
    #     for selection in selections:
    #         self.focus(selection)
    #         selection.click()
    #         sleep(1)
    #     selections = self.browser.find_elements_by_xpath(self.commentInputSubXpath)
    #     for selection in selections:
    #         self.focus(selection)
    #         query = Tell.comment[randint(0,len(Tell.comment)-1)]
    #         say = query.format(Tell.smiley[randint(0,len(Tell.smiley)-1)])
    #         selection.send_keys(say)
    #         selection.send_keys(Keys.RETURN)
    #         sleep(10)

    # def author(self,post):
    #     return post.find_element_by_xpath(self.userNameSubXpath).text

    # def commentPost(self,post):
    #     print("Commenting post.")
    #     selection = post.find_element_by_xpath(self.commentButtonSubXpath)
    #     self.focus(selection)
    #     selection.click()
    #     sleep(1)
    #
    #     query = Tell.comment[randint(0,len(Tell.comment)-1)]
    #     say = query.format(self.author(post),Tell.smiley[randint(0,len(Tell.smiley)-1)])
    #
    #     selection = post.find_element_by_xpath(self.commentInputSubXpath)
    #     selection.send_keys(say)
    #     selection.send_keys(Keys.RETURN)

    def returnAvailableMenus(self):
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')

        return self.browser.find_elements_by_xpath(self.aliasSelectionSubXpath)

    def doSomeMagic(self):
        if self.mailer.getCurrentMessage() == "Stop":
            raise Exception('Stopped by telegram.')

        self.loginToFacebook()
        while True:
            for topic in self.topics:
                self.mailer.sendMessage("Selecting next topic: "+topic)
                posts = self.getPostsFromHashtagPage(topic)
                # availableMenus = self.returnAvailableMenus()
                # currentmenu = 1
                # totalMenus = len(availableMenus)
                # for menu in availableMenus:
                #     self.mailer.sendMessage("Switching to Alldaycreative. ("+str(currentMenu)+"/"+str(totalMenus)+")")
                #     self.selectAlldaycreative(menu)
                #     currentMenu += 1
                self.likeEverything()
                self.sendStats()
                # self.commentEverything()

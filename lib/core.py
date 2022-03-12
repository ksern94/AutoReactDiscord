import logging
import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import chromedriver_binary  # Adds chromedriver binary to path

logging.getLogger().setLevel(logging.WARNING)

class AutoDiscord:
    """
    This is a bot to automatically react to NFT giveaways across multiple discord guild/server
    """

    def __init__(self):
        pass
    # end def
    
    def wait(self, delay=1):
        """
        Delay method, in seconds
        """
        time.sleep(delay)
    # end def

    def launch_browser(self, isHeadless = False):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if(isHeadless):
            options.headless = True
        #end if

        browser = webdriver.Chrome(options=options)

        return browser
    #  end def

    def go_to_discord_server(self, browser, url):
        # go to server/giveaway channel
        browser.get(url)

        # browser.execute_script("document.body.style.zoom='67%'")
        self.wait()
        print(browser.current_url)
        if "https://discord.com/login" in browser.current_url:
            # not logged in yet
            self.log_in(browser)


        # find chatContent-* element
        self.wait(10) 
        try:
            chatContent = browser.find_element(by=By.CSS_SELECTOR, value="main[class^='chatContent-']")
            logging.info('💻 chatContent found.')
        except NoSuchElementException:
             # TBD : retry x number of times
             logging.info('💻 chatContent not found.')
        # end try

        # find last message
        try:
            messages = chatContent.find_elements(by=By.CSS_SELECTOR, value="li[class^='messageListItem-']")
            lastMessagesList = messages[-3:]

            # print(lastMessage.get_attribute('outerHTML'))
            logging.info('💻 lastMessagesList found.')
        except NoSuchElementException:
            logging.info('💻 messages not found.')
        # end try
        
        # check last x number of messages
        messageCounter = 0
        for lastMessage in lastMessagesList:
            print(f"Message counter: {messageCounter}")
            logging.info('💻 start processing messages.')
            # check message content
            # find author
            # find botTag
            # check message author == bot + giveaway
            isGiveaway = True
            try:
                content = lastMessage.find_element(by=By.CSS_SELECTOR, value="div[class^='contents-']")
                messageAuthor = content.find_element(by=By.CSS_SELECTOR, value="h2 span[id^='message-username'] span[class^='username-']").get_attribute('innerText')

                logging.info(f"Message Author: {messageAuthor}")

                # if not giveaway bot we dont react
                giveawayBotName = ["giveaway"]
                if any(dict not in messageAuthor.lower() for dict in giveawayBotName):
                    isGiveaway = False

                # if "giveaway" not in messageAuthor.lower():
                #     isGiveaway = False

            except NoSuchElementException:
                logging.info('💻 messageAuthor not found.')
            # end try

            try:
                botTag = content.find_element(by=By.CSS_SELECTOR, value="h2 span[id^='message-username'] span[class^='botText-']").get_attribute('innerText')
                logging.info(f"Message bot tag: {botTag}")
            except NoSuchElementException:
                isGiveaway = False
                logging.info('💻 botTag not found.')

            # message content
            try:
                messageContent = content.find_element(by=By.CSS_SELECTOR, value="div[id^='message-content']").get_attribute('innerText')

                logging.info(f"checking message content: {messageContent}")

                # list of keyword to filter
                giveawayEndedList = ["grat","congratulation","ended"]
                if any(dict in messageContent.lower() for dict in giveawayEndedList):
                    isGiveaway = False

            except NoSuchElementException:
                logging.info('💻 messageContent not found.')
            # end try

            if(isGiveaway):
                # find reaction button
                # react to message
                try:
                    messageAccessories = lastMessage.find_element(by=By.CSS_SELECTOR, value="div[id^='message-accessories-']")

                    logging.info("Message accessories found")
                except NoSuchElementException:
                    logging.info('💻 messageAccessories not found.')
                # end try

                # check if there is existing reactions
                try:
                    reactionGroup = messageAccessories.find_element(by=By.CSS_SELECTOR, value="div[id^='message-reactions-']")

                    logging.info("Reaction Group found")
                except NoSuchElementException:
                    logging.info('💻 reactionGroup not found.')
                # end try

                isGiveawayReacted = False
                # check reactions
                try:
                    reactions = reactionGroup.find_elements(by=By.CSS_SELECTOR, value="div[class^='reaction-']")

                    logging.info("reactions found")

                    # press on :tada: reactions 
                    # https://discord.com/assets/b052a4bef57c1aa73cd7cff5bc4fb61d.svg
                    for reaction in reactions:
                        self.wait(1)
                        reactionInner = reaction.find_element(by=By.CSS_SELECTOR, value="div[class^='reactionInner-']")
                        isPressed = reactionInner.get_attribute("aria-pressed")

                        if(isPressed == 'false'):
                            # check if emoji is :tada:
                            emojiImgSrc = reactionInner.find_element(by=By.CSS_SELECTOR, value="img").get_attribute("src")
                            
                            # if it's :tada: emoji
                            if(emojiImgSrc == "https://discord.com/assets/b052a4bef57c1aa73cd7cff5bc4fb61d.svg"):
                                #click it
                                reactionInner.click()
                                isGiveawayReacted = True
                            # end if
                        else:
                            isGiveawayReacted = True
                        #end if
                    # end for
                except NoSuchElementException:
                    logging.info('💻 reactions not found.')
                # end try

                logging.info(f'💻 isGiveawayReacted: {isGiveawayReacted}')
                if(isGiveawayReacted == False):
                    self.wait(5)
                    # did not have existing reaction
                    # we need to find the emoji and react
                    logging.info("moving to element")

                    # doing this twice to make sure it happen
                    ActionChains(browser).move_to_element(lastMessage).perform() #hover
                    ActionChains(browser).move_to_element(lastMessage).perform() #hover

                    try:
                        self.wait(3)
                        buttonContainer = lastMessage.find_element(by=By.CSS_SELECTOR, value="div[class^='buttonContainer-']")
                        addReactionButton = buttonContainer.find_element(by=By.CSS_SELECTOR, value="div[aria-label='Add Reaction']")
                        addReactionButton.click()

                        self.wait(2)
                        emojiPickerTab = browser.find_element(by=By.CSS_SELECTOR, value ="div[id='emoji-picker-tab-panel']")
                        emojiSearchBar = emojiPickerTab.find_element(by=By.CSS_SELECTOR, value ="input[type='text']")
                        emojiSearchBar.send_keys(":tada:")
                        self.wait(2) #buffer
                        emojiSearchBar.send_keys(Keys.ENTER)
                    except NoSuchElementException:
                        logging.info("error reacting to message")
                    #end try
                #end if
            #end if

            messageCounter += 1
        # end if
    # end def

    def log_in(self, browser):
        """
        Logs user into discord
        """
        print('🔑 Logging in')

         # Loads user configurations from config.json
        with open('config.json', 'r') as u:
            config = json.load(u)
        # end with
        username = config["credentials"]["username"]
        # print(username)
        password = config["credentials"]["password"]

        browser.find_element_by_name('email').send_keys(username)
        browser.find_element_by_name('password').send_keys(password)
        browser.find_element_by_name('password').send_keys(Keys.ENTER)

        self.wait(3)
        # print(browser.current_url)
        if "https://discord.com/channels" in browser.current_url:
            logging.info('🔓 Successfully logged in')
        else: 
            logging.info('🔓 Failed to log in')
        #end if
    # end def


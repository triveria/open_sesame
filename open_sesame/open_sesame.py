"""
For now, this only works with WhatsApp.
You send a WhatsApp message to a number you own and scrape the whatsapp chat via selenium and whatsapp-web.
In response a MQTT message is sent to your smart door.
"""

# ref.: https://stackoverflow.com/questions/65299796/how-do-i-read-whatsapp-messages-from-a-contact-using-python
# ref.: https://highontechs.com/chatbot/read-whatsapp-messages-using-python-selenium/

#TODO: use relais to control door strikes
#TODO: make full program via cookiecutter: run, add --name="Gast" --expires=+6h
#TODO: add ESP project as submodule
#TODO: translate responses


from . import helpers as h
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def enter_chat(driver, sender):
    whatsapp_search_css = "#side._1KDb8 > div.uwk68 > div._3yWey label._1Jn3C > div._1UWac._3hKpJ > div._13NKt.copyable-text.selectable-text"
    search = driver.find_element(By.CSS_SELECTOR, whatsapp_search_css)
    search.send_keys(sender + Keys.ENTER)


def leave_chat(driver):
    ini = h.load_ini()
    dummy_contact = ini["MAIN"]["dummy_contact"]
    enter_chat(driver, dummy_contact)


def get_unread_chats(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    chats = soup.find_all("div", class_="_3OvU8")
    senders = []

    for chat in chats:
        unread_message = chat.find("div", class_="_1pJ9J")
        if unread_message:
            sender = chat.find("span", class_="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr").text
            senders.append(sender)
            enter_chat(driver, sender)
            leave_chat(driver)

    return senders


def check_for_new_messages(driver):
    allow_list = h.load_allow_list()
    senders = get_unread_chats(driver)
    for sender in senders:
        if h.is_access_granted(sender, allow_list):
            h.open_door()
            print(f"{sender} has opened the door")
        else:
            print(f"{sender} has tried to enter")


def main():
    ini = h.load_ini()
    firefox_profile_filepath = ini["MAIN"]["firefox_profile"]
    fp = webdriver.FirefoxProfile(firefox_profile_filepath)
    driver = webdriver.Firefox(fp)
    driver.get("https://web.whatsapp.com")
    time.sleep(10)

    print("WhatsApp started")

    while True:
        check_for_new_messages(driver)
        time.sleep(1)

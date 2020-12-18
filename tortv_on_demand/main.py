import names
import time
import os

import re
import requests
from tortv_on_demand.captcha_reco import read_captcha
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from tortv_on_demand.tempmail import NADA
from pathlib import Path
from .categories import CATEGORIES


def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(0.15)


def rm_tree(pth: Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def process(show_browser: bool, categories: list):
    """

    :param show_browser:
    :param categories:
    :return:
    """
    for c in categories:
        if c not in CATEGORIES:
            raise RuntimeError("The category ->"+str(c)+" is not available,"
                               "please choose from the following list: "
                               + str(list(CATEGORIES.keys())))
    mailclient = NADA()

    if show_browser:
        browser = Chrome()
    else:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = Chrome(chrome_options=chrome_options)
    browser.get('https://tortv.live/auth/registration/')

    # crack captcha here
    captcha_image = browser.find_element_by_xpath("//img")
    captcha_image_url = captcha_image.get_attribute("src")

    r = requests.get(captcha_image_url)
    tmp_dir = Path("./tmp")
    tmp_dir.mkdir(exist_ok=True)
    with open("./tmp/current.jpg", "wb") as f:
        f.write(r.content)
    captcha_code = read_captcha("./tmp/current.jpg")
    print("captcha code found :", captcha_code)
    rm_tree(Path("./tmp"))
    my_name = names.get_full_name()
    my_password = "azerty"
    my_email = mailclient.getData()

    forms = {
        "//input[@name='name']": my_name,
        "//input[@name='email']": my_email,
        "//input[@name='password']": my_password,
        "//input[@name='token']": captcha_code
    }

    for key, value in forms.items():
        current = browser.find_element_by_xpath(key)
        if show_browser:
            slow_typing(current, value)
            time.sleep(1)
        else:
            current.send_keys(value)

    browser.find_element_by_xpath("//button").click()
    time.sleep(3)
    browser.close()

    messages = mailclient.getMessages()  # Get messages
    try:
        latest_message_id = messages[0][0][0]

        url = "https://getnada.com/api/v1/messages/html/" + latest_message_id
        res = requests.get(url)
        email_verif = \
            re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', res.text)[0]
        print("email verification ", email_verif)
    except:
        print("No new messages")
        email_verif = "https://tortv.live/auth/login"

    # Click verif email

    # Second connection
    if show_browser:
        browser = Chrome()
    else:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = Chrome(chrome_options=chrome_options)
    browser.get(email_verif)

    time.sleep(3)

    # username / password
    signin = {
        "//input[@name='email']": my_email,
        "//input[@name='password']": my_password,
    }
    for key, value in signin.items():
        current = browser.find_element_by_xpath(key)
        slow_typing(current, value)
        time.sleep(1)

    browser.find_element_by_xpath("//button").click()

    time.sleep(2)
    selected_categories = {}

    for c in categories:
        selected_categories[c] = CATEGORIES[c]
    if len(selected_categories.keys()) == 0:
        raise RuntimeError("No categorie specified !")

    print("Selected Channels categories : ", list(selected_categories.keys()))

    for cat in selected_categories.keys():
        xpath = "//input[@value='" + str(selected_categories[cat]) + "']"
        browser.find_element_by_xpath(xpath).click()

    browser.find_element_by_xpath("//button").click()

    pattern = "type=m3u&output=ts"
    all_links = browser.find_elements_by_xpath("//a")

    vlc_link = [l for l in all_links if pattern in l.get_attribute("href")]
    m3u_url = vlc_link[0].get_attribute("href")

    print("Will download the following m3u file:")
    print(m3u_url)

    if len(vlc_link) == 0:
        raise RuntimeError("Cannot find VLC m3u")

    output_name = "TV.m3u"

    with requests.get(m3u_url, stream=True) as r:
        with open(output_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    print("Successfully saved the m3u8 !!")
    print("You can now open the file " + str(os.getcwd()) + "/" + output_name + " using VLC and enjoy ;)")

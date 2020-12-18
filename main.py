from tempmail import NADA
from captcha_reco import read_captcha
from selenium.webdriver import Chrome
import time, names
import requests, re
import numpy, cv2

def slow_typing(element, text):
   for character in text:
      element.send_keys(character)
      time.sleep(0.15)

mailclient = NADA()

browser = Chrome()
browser.get('https://tortv.live/auth/registration/')
print(browser.title)

# crack captcha here
captcha_image = browser.find_element_by_xpath("//img")
captcha_image_url = captcha_image.get_attribute("src")
print(captcha_image_url)

r = requests.get(captcha_image_url)
with open("current.jpg", "wb") as f:
    f.write(r.content)

captcha_code = read_captcha('current.jpg', './templates/') 
my_name = names.get_full_name()
my_password = "azerty"
my_email = mailclient.getData()

forms = {
    "//input[@name='name']" : my_name,
    "//input[@name='email']" : my_email,
    "//input[@name='password']" : my_password,
    "//input[@name='token']" : captcha_code
}

for key, value in forms.items():
    print(key, value)
    current = browser.find_element_by_xpath(key)
    slow_typing(current, value)
    time.sleep(1)

browser.find_element_by_xpath("//button").click()
time.sleep(5)
browser.close()

time.sleep(10)

messages = mailclient.getMessages()	#Get messages
print(messages)
try:
    latest_message_id = messages[0][0][0]

    url = "https://getnada.com/api/v1/messages/html/" + latest_message_id
    res = requests.get(url)
    email_verif = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', res.text)[0]
    print(email_verif)
except:
    print("No new messages")
    email_verif = "https://tortv.live/auth/login"

# Click verif email

# Second connection
browser = Chrome()
browser.get(email_verif)

time.sleep(3)

# username / password
signin = {
    "//input[@name='email']" : my_email,
    "//input[@name='password']" : my_password,
}
for key, value in signin.items():
    print(key, value)
    current = browser.find_element_by_xpath(key)
    slow_typing(current, value)
    time.sleep(1)

browser.find_element_by_xpath("//button").click()

time.sleep(5)

# check category checkboxes

categories = {
    "france" : 11,
    "sport" : 12
}

for cat in categories.keys():
    xpath = "//input[@value='" + str(categories[cat]) + "']"
    browser.find_element_by_xpath(xpath).click()

browser.find_element_by_xpath("//button").click()

pattern = "type=m3u&output=ts"
all_links = browser.find_elements_by_xpath("//a")

print("all links:")
print(all_links)

vlc_link = [l for l in all_links if pattern in l.get_attribute("href")]
m3u_url = vlc_link[0].get_attribute("href")

print("vlc links 0")
print(m3u_url)

if len(vlc_link) == 0:
    raise RuntimeError("Cannot find VLC m3u")

with requests.get(m3u_url, stream=True) as r:
    with open("wind-turbine.m3u", "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
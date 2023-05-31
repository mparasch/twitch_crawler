from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import datetime
from chat_downloader import ChatDownloader
from selenium.webdriver.remote.utils import format_json

# importing current date to name videos
today = datetime.datetime.today()
year, month, day = today.year, today.month, today.day

url = 'https://www.twitch.tv/directory/game/Fortnite/clips?range=24hr'

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)

for n in range(5): #after we need to scroll an entire screen after every twenty -- scroller not working

    driver.get(url)
    time.sleep(2)
    clips = driver.find_elements_by_css_selector('.sc-AxjAm.iOGWRP')
    clips[n].click()
    time.sleep(5)

    clip_url = driver.current_url

    try:
        # USE VIDEO ID FOR IDENTIFICATION
        ChatDownloader().get_chat(url=clip_url, output='./data/{}_{}_clip.json'.format(str(year)+str(month)+str(day), n))
        
        full_stream = driver.find_element_by_css_selector('a[data-test-selector="clips-watch-full-button"]')
        fs_url = full_stream.get_attribute('href')
        print(fs_url)

        if full_stream:
            full_stream.click()
            time.sleep(5)
            share = driver.find_element_by_css_selector('button[aria-label="Share"]')
            share.click()

            text = driver.find_element_by_css_selector('input[data-a-target="tw-input"][class="ScInputBase-sc-1wz0osy-0 ScInput-m6vr9t-0 fJhImV FJRwf InjectLayout-sc-588ddc-0 tw-input"')

            fs_url = str(text.get_attribute('value'))

            ChatDownloader().get_chat(url=fs_url, output='./data/{}_{}_full.json'.format(str(year)+str(month)+str(day), n))
    except:
        pass


driver.close()


def twtich_login(driver=driver):
    user = '<USERNAME>'
    pw = '<USER PASS>'

    driver.get('https://www.twitch.tv/')
    login_class = '.ScCoreButton-sc-1qn4ixc-0.ScCoreButtonSecondary-sc-1qn4ixc-2.iDPpfj'
    login = driver.find_element_by_css_selector(login_class)
    login.click()
    time.sleep(5)

    uname = driver.find_element_by_id('login-username')
    uname.send_keys(user)

    pword = driver.find_element_by_id('password-input')
    pword.send_keys(pw)

    send = driver.find_element_by_css_selector('.sc-AxjAm.jTWfwi')
    send.click()

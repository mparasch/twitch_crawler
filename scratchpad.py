from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from chat_downloader import ChatDownloader
from selenium.webdriver.remote.utils import format_json
import json

main_url = 'https://www.twitch.tv/directory/game/Fortnite/clips?range=24hr'

options = Options()
# options.headless = True

driver = webdriver.Firefox(options=options)

driver.get(main_url)
time.sleep(2)

page = driver.find_element_by_css_selector('a[class="sc-fznMAR kIMkAW bccfYP sc-AxheI tw-link"]')
clip_count = 0
max_clips = 50

while clip_count < max_clips:
    page.send_keys(Keys.END)
    time.sleep(3)
    clip_count = len(driver.find_elements_by_css_selector('a[data-a-target="preview-card-image-link"]'))


clips = driver.find_elements_by_css_selector('a[data-a-target="preview-card-image-link"]')

clips_url = []
for clip in clips:
    clips_url.append(clip.get_attribute('href'))

for url in clips_url:
    driver.get(url)
    time.sleep(4)

    try:
        full_stream = driver.find_element_by_css_selector('a[data-test-selector="clips-watch-full-button"]')
        fs_url = full_stream.get_attribute('href')
        stream_id = fs_url.split('/')[4].split('?')[0]
        clip_time = fs_url.split('=')[-1]

        views = driver.find_element_by_css_selector('div[data-a-target="tw-stat-value"]').text

        clip_chat = ChatDownloader().get_chat(url)

        with open('./data/{}_{}_clip.json'.format(stream_id, clip_time), 'w') as fp:
            for message in clip_chat:
                json.dump(message, fp)

        # WILL BE ENABLED WHEN WE START COLLECTING FULL VIDEO DATA
        # stream_chat = ChatDownloader().get_chat(url=fs_url, output='./data/{}_full.json'.format(stream_id))

        # with open('./data/{}_full.json'.format(stream_id), 'w') as fp:
        #     for message in stream_chat:
        #         json.dump(message, fp)

    except:
        pass

driver.close()
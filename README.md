# Twitch Clip Scraper

## Overview
This script uses Selenium and the `chat_downloader` library to scrape Twitch clips within a 24-hour range. It retrieves the URLs and metadata (such as views and length) for the clips, as well as the associated chat data. The script can download individual clip data and save it to JSON files, including the chat messages from the clip and metadata about the clip itself.

## Requirements
To run this script, you need the following Python packages:
- `selenium`
- `chat_downloader`
- `json`
- `firefox` (and the `geckodriver` to use Selenium with Firefox)

Additionally, make sure that geckodriver is installed for Firefox:
* [Download Geckodriver](https://github.com/mozilla/geckodriver/releases)

## Functionality
1. **Initialize WebDriver**
   
The script initializes a Firefox WebDriver with headless options (optional) to interact with the Twitch website. It opens the main URL for Fortnite clips within the last 24 hours.
```python
driver = webdriver.Firefox(options=options)
driver.get(main_url)
```

2. **Scroll to Load More Clips**
   
Using Selenium, the script sends the END key to the browser to scroll down the page, allowing more clips to load. This process continues until the script reaches the specified max_clips count.
```python
page.send_keys(Keys.END)
time.sleep(5)
```

3. **Extract Clip Metadata**

For each clip, the script extracts the following metadata:
URL: Link to the clip
Length: Duration of the clip
Views: Number of views for the clip
This data is stored in a list and converted into a Pandas DataFrame for further processing.
```python
clips = driver.find_elements_by_css_selector('a[data-a-target="preview-card-image-link"]')[0:max_clips]
```

4. **Download Chat Data for Each Clip**
   
For every clip, the script navigates to its page and downloads the associated chat messages using ChatDownloader. The chat messages are saved in JSON format, with the file name based on the stream ID and clip timestamp.
```python
clip_chat = ChatDownloader().get_chat(clip['url'])
with open('./data/{}_{}_clip.json'.format(stream_id, clip_time), 'w') as fp:
    for message in clip_chat:
        json.dump(message, fp)
```

5. **Save Clip Metadata**
   
The script also gathers additional metadata such as the full stream URL (if available) and the clip's views. This data is saved in a separate JSON file for each clip.
```python
data = {
    'full_stream':{
        'id':stream_id,
        'url':fs_url,
    },
    'clip':{
        'url':clip['url'],
        'views':views,
        'length':clip['length']
    }
}
with open('./data/{}_{}_meta.json'.format(stream_id, clip_time), 'w') as fp:
    json.dump(data, fp)
```

6. **Full Video Data (Optional)**
   
The script includes commented-out code that can be enabled to download chat data for the full stream of a clip. This feature is optional and can be activated by uncommenting the relevant code.
```python
# stream_chat = ChatDownloader().get_chat(url=fs_url, output='./data/{}_full.json'.format(stream_id))
```

## Script Flow
Navigate to Twitch Page: The script opens the main URL for Fortnite clips on Twitch.
Scroll to Load More Clips: It scrolls down to load additional clips until the limit (max_clips) is reached.
Extract Clip Data: Metadata and chat data for each clip are extracted.
Download Chat Data: Chat messages for each clip are downloaded and saved in a JSON file.
Save Metadata: Metadata, including stream URLs, views, and lengths, is saved in separate JSON files.
Optional Full Stream Data: The script can also download chat data for full streams if enabled.

## Execution
1. Install the required dependencies.
2. Ensure that geckodriver is installed and accessible in your system's PATH.
3. Run the script, which will scrape the clips from Twitch and save them locally in JSON format.
```bash
python twitch_clip_scraper.py
```

## Notes
* Headless Mode: The Firefox browser can run in headless mode by uncommenting the options.headless = True line. This prevents the browser from opening visually.
* Error Handling: The script has basic error handling to skip over any clips that cannot be processed.
* Rate Limiting: The script includes time.sleep() calls to prevent overwhelming the server by sending requests too quickly. This helps reduce the risk of being blocked by Twitch.

## License
This script is for educational and personal use. Ensure compliance with Twitch’s Terms of Service when using the script for scraping or downloading content.

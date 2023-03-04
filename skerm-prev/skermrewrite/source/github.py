import json
import time
import requests

from source import parser, webhook, logger

CURRENT_KEY = 0
RETRY_COUNT = 0
MAX_RETRY_COUNT = 5

API_URL = "https://api.github.com"
RAW_URL = "https://raw.githubusercontent"

with open('config.json', 'r') as f:
    config = json.load(f)

api_keys = config['github']['api_keys']
search_parameter = config['github']['search_parameter']
retry_wait_time = 15

def search():
    global CURRENT_KEY
    global RETRY_COUNT

    RETRY_COUNT = 0

    api_key = api_keys[CURRENT_KEY]
    headers = {'Authorization' : f'Token {api_key}'}

    while RETRY_COUNT < MAX_RETRY_COUNT:
        try:
            response = requests.get(f"{API_URL}/{search_parameter}", headers=headers, timeout=5000)
            response.raise_for_status()
            return response.json()
        except:
            RETRY_COUNT += 1
            logger.error("Request failed, retrying in 15 seconds")
            time.sleep(retry_wait_time)

    CURRENT_KEY += 1

    if CURRENT_KEY == len(api_keys):
        CURRENT_KEY = 0

def get_content(data: dict) -> list:
    """Getting raw links from API response"""
    links = {}
    new_links = []

    with open("source/resources/github_cache", "r", encoding="UTF-8") as file:
        existing_links = set(line.strip() for line in file)

    for i in data['items']:
        link = f"{RAW_URL}{i['html_url'][14:]}"
        link = link.replace('/blob', '')

        if link not in existing_links:
            new_links.append(link)
            links[link] = "GITHUB"

    if new_links:
         with open('source/resources/github_cache', 'a', encoding="UTF-8") as file:
            if existing_links:
                file.write("\n")
            file.write("\n".join(new_links))
       
    return links

def scrape() -> None:
    """Used to perform all functions from scraping the api to sending messages to the webhook"""
    data = search()
    links = get_content(data)


    webhooks = parser.parse(links)
    webhook.list_send(webhooks)
    
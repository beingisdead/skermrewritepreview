import json
from requests_html import HTMLSession
from source import parser, webhook, logger
#from program import curses

#Will be ran in seperate thread?

session = HTMLSession()

def getarchive():
    links = {}
    new_links = []

    with open("source/resources/pastebin_cache", "r", encoding="UTF-8") as file:
        existing_links = set(line.strip() for line in file)

    response = session.get('https://pastebin.com/archive')      
    maintable = response.html.find('html body.night-auto div.wrap div.container div.content div.page.page-archive.-top div.archive-table table.maintable tbody tr td a')
    
    for i in maintable:
        if "archive" not in i.attrs.get('href'):
            link = f"https://pastebin.com/raw{i.attrs['href']}"
            if link not in existing_links:
                new_links.append(link)
                links[link] = "PASTEBIN"

    if new_links:
         with open('source/resources/pastebin_cache', 'a', encoding="UTF-8") as file:
            if existing_links:
                file.write("\n")
            file.write("\n".join(new_links))
    return links

def scrape() -> None:
    """Used to perform all functions from scraping the api to sending messages to the webhook"""
    links = getarchive()
    webhooks = parser.parse(links)
    webhook.list_send(webhooks)
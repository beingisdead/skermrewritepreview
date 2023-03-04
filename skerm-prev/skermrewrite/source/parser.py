import requests
import json
import re

from source import logger
sent_webhooks = []

def get_content(links) -> dict:
    content = {}

    for url, source in links.items():
        content.setdefault(source, []).append({requests.get(url).text: url})

    return content

def search_text(content) -> dict:
    """Use regex to search content for potential webhooks"""
    
    webhooks = {match.group(0): {source: url} for source, text in content.items() for i in text for text, url in i.items() if (match := re.search("https:\/\/discord.com\/api\/webhooks\/([0-9\/]+)\/([\w-]+)\w", text))}
    return webhooks

def parse(links) -> list:
    content = get_content(links)
    webhooks = search_text(content)
    
    return webhooks
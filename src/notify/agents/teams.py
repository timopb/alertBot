from src.abstraction.interface import IFaceNotify
import logging
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger("alertBot.teams")


class Teams(IFaceNotify):
    def __init__(self, config):
        # self.dest = config.destinations
        self.url = config.url

    def send_notification(self, msg, title: str):
        facts = []
        if isinstance(msg, dict):
             for key in msg:
                  facts.append({ "name": key, "value": msg[key] })
             msg = msg["name"]

        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Suricata Security Alert",
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": msg,
                "facts": facts,
                "markdown": True
            }]
        }


        r = requests.post(url=self.url, json=payload)
        if r.status_code != 200:
            logger.warning("Webhook response code !=200. Status code: %d", r.status_code)
            return False
        return True

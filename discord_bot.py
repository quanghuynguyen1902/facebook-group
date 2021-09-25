from discord import Webhook, RequestsWebhookAdapter
import os
from dotenv import load_dotenv

load_dotenv()

# Webhook of my channel. Click on edit channel --> Webhooks --> Creates webhook
mUrl = os.getenv("webhook")


def send_message(message):
    webhook = Webhook.from_url(mUrl, adapter=RequestsWebhookAdapter())
    webhook.send(message)
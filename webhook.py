from discord import Webhook, RequestsWebhookAdapter

def SendMessage(message, token):
    webhook = Webhook.from_url(str(token), adapter=RequestsWebhookAdapter())
    webhook.send(message)
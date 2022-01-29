from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class LaukopierPost(DiscordEmbed):
    discord_channel = os.getenv("POSTS_WEBHOOK")

    def __init__(self, title, url):
        super().__init__(title="New Laukopier Post", color="03b2f8")
        self.set_timestamp()
        self.add_embed_field(name=title, value=url)

        webhook = DiscordWebhook(LaukopierPost.discord_channel)
        webhook.add_embed(self)
        webhook.execute()


class LaukopierError(DiscordEmbed):
    discord_channel = os.getenv("POSTS_WEBHOOK")

    def __init__(self, message):
        super().__init__(title="Laukopier Error", color="FF0000")
        self.set_timestamp()
        self.add_embed_field(name="Message", value=message)

        webhook = DiscordWebhook(LaukopierError.discord_channel)
        webhook.add_embed(self)
        webhook.execute()

import asyncio
import os
from datetime import datetime, timedelta, timezone
from time import sleep

import aiohttp
import feedparser
from discord import Colour, Embed, Webhook
from dotenv import load_dotenv
from markdownify import markdownify

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK")
RSS = os.getenv("RSS")

rss_db = set()


async def main():
    data = feedparser.parse(RSS)
    provider = data.feed.title
    for entry in data.entries:
        if entry.link not in rss_db:
            title = entry.title
            link = entry.link
            description = markdownify(entry.summary)
            author = entry.author

            embed = Embed()
            embed.title = title
            embed.colour = Colour.darker_grey()
            embed.description = description
            embed.timestamp = datetime.now(timezone(timedelta(hours=+8)))
            embed.set_author(name=provider + " ( " + author + " )")
            embed.set_footer(
                text="Powered by abe-101",
                icon_url="https://github.com/abe-101.png",
            )
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(WEBHOOK_URL, session=session)
                await webhook.send(content=f"{title}\n{link}", embed=embed)
            rss_db.add(link)


def populate_db():
    data = feedparser.parse(RSS)
    for i in data.entries:
        rss_db.add(i.link)


if __name__ == "__main__":
    populate_db()
    while True:
        asyncio.run(main())
        sleep(30)

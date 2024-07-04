import google.generativeai as gai
import asyncio
from pyppeteer import launch

import config

url = "https://www.google.com/maps/place/Their+There/@49.267915,-123.1540049,17z/data=!4m12!1m2!2m1!1sgoogle+maps+their+there!3m8!1s0x548673586fb2b94f:0xe55cc57f1c5a41b0!8m2!3d49.267915!4d-123.15143!9m1!1b1!15sChdnb29nbGUgbWFwcyB0aGVpciB0aGVyZSIDiAEBkgERYnJ1bmNoX3Jlc3RhdXJhbnTgAQA!16s%2Fg%2F11g0g5sntw?entry=ttu"

async def scrape_reviews(url: str):
    browser = await launch({"headless": False, "args": ["--window-size=800,3200"]})

    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)

asyncio.get_event_loop().run_until_complete(scrape_reviews(url))
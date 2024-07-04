import google.generativeai as gai
import asyncio
from pyppeteer import launch

import config

url = "https://www.google.com/maps/place/Their+There/@49.267915,-123.1540049,17z/data=!4m12!1m2!2m1!1sgoogle+maps+their+there!3m8!1s0x548673586fb2b94f:0xe55cc57f1c5a41b0!8m2!3d49.267915!4d-123.15143!9m1!1b1!15sChdnb29nbGUgbWFwcyB0aGVpciB0aGVyZSIDiAEBkgERYnJ1bmNoX3Jlc3RhdXJhbnTgAQA!16s%2Fg%2F11g0g5sntw?entry=ttu"

async def scrape_reviews(url: str):
    # Set headless to true if you want Chromium to open up a window
    browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})
    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)

    # This is the class for a review (.jftiEf)
    await page.waitForSelector(".jftiEf")

    # Get all the review text
    elements = await page.querySelectorAll(".jftiEf")

    for element in elements:
        # This is the class for a reviewer (.MyEned)
        await page.waitForSelector(".MyEned")
        reviwer = await element.querySelector(".MyEned")
        # Note: these review texts are in a class called .wiI7pd
        review = await page.evaluate('(element) => element.textContent', reviwer)
        print(review)

    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape_reviews(url))
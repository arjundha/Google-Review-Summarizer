import google.generativeai as genai
import asyncio
from pyppeteer import launch

import config

url = "https://www.google.com/maps/place/Their+There/@49.267915,-123.1540049,17z/data=!4m12!1m2!2m1!1sgoogle+maps+their+there!3m8!1s0x548673586fb2b94f:0xe55cc57f1c5a41b0!8m2!3d49.267915!4d-123.15143!9m1!1b1!15sChdnb29nbGUgbWFwcyB0aGVpciB0aGVyZSIDiAEBkgERYnJ1bmNoX3Jlc3RhdXJhbnTgAQA!16s%2Fg%2F11g0g5sntw?entry=ttu"

async def scrape_reviews(url: str):
    reviews = []
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
        # Try to click on a "more" button if it exists via class .w8nwRe or .kyuRq
        try:
            more_button = await element.querySelector(".w8nwRe")
            await more_button.click()
        except:
            pass
        # This is the class for a reviewer (.MyEned)
        await page.waitForSelector(".MyEned")
        reviwer = await element.querySelector(".MyEned")
        # Note: these review texts are in a class called .wiI7pd
        review = await element.querySelector(".wiI7pd")
        review = await page.evaluate('(element) => element.textContent', review)
        reviews.append(review)

    await browser.close()
    return reviews

def summarize_reviews(reviews: list, model):
    prompt = "Here are some reviews collected from a place I wanted to visit. Can you summarize them for me? After, can you try to give me three pros and three cons? The reviews are as follows:\n"

    for review in reviews:
        prompt += "\n" + review

    response = model.generate_content(prompt)

    return response


def main():
    genai.configure(api_key=config.API_KEY)
    model = genai.GenerativeModel("gemini-1.0-pro")
    reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))
    result = summarize_reviews(reviews, model)
    print(result)

if __name__ == "__main__":
    main()
import google.generativeai as genai
import asyncio
from pyppeteer import launch

import config

async def scrape_reviews(place: str, city: str):
    reviews = []

    # Set headless to true if you want Chromium to open up a window
    browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})
    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})

    # Use Google Maps to try and find the place of interest
    await page.goto("https://www.google.com/maps")
    await page.type("input#searchboxinput", f"{place} {city}")
    await page.keyboard.press("Enter")

    # Wait for the page to load
    await page.waitForNavigation()
    await page.waitForSelector(".RWPxGd")

    # Click the Reviews tab
    await page.click(".hh2c6[data-tab-index='1']")

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
    prompt = """Here are some reviews collected from a place I wanted to visit. Can you summarize them for me? 
    After that, can you try to give me three pros and three cons? The reviews are as follows:\n"""

    for review in reviews:
        prompt += "\n" + review

    # print(prompt)

    response = model.generate_content(prompt, stream=True)
    text = ""
    for chunk in response:
        # print(chunk.text)
        text += chunk.text
    return text


def main():
    # Model Configuration
    genai.configure(api_key=config.API_KEY)
    model = genai.GenerativeModel("gemini-1.0-pro")

    # Get User Input
    print("Hello! I am a program which can be used to summarize the Google Reviews of a location. I will need the name, and the location of the place you want to visit in order to do so!")
    place = input("\nWhat is the name of the place you want to visit?: ")
    city = input("\nWhat city is this place located in? (You may also wish to include the country, state, province, or county to get accurate results): ")
    print(f"\nThank you! I will now generate a summarized review of {place} for you!\nPlease wait...\n")
    # Scrape Reviews and Summarize
    reviews = asyncio.run(scrape_reviews(place, city))
    result = summarize_reviews(reviews, model)
    print(result)

if __name__ == "__main__":
    main()
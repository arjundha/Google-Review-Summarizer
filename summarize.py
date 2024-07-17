from pyppeteer import launch
from dotenv import load_dotenv
from pprint import pprint

import google.generativeai as genai
import asyncio
import os
import requests

import helpers.review_scraper

load_dotenv()


async def scrape_reviews(place: str, city: str):
    reviews = []

    # Set headless to true if you want Chromium to open up a window
    # browser = await launch({"headless": False, "dumpio": True})

    browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
    page = await browser.newPage()
    await helpers.review_scraper.load_browser(page, place, city)

    # Find the first result
    await helpers.review_scraper.find_first_result(page)

    # See if there is a result to click on
    try:
        title = await helpers.review_scraper.get_location_title(page)
        if not title or not helpers.review_scraper.does_title_contain_location(
            title, place
        ):
            raise Exception("No location title found")
        print("Location title found!")
        print(title)
        await helpers.review_scraper.click_reviews_tab(page)
    except:
        await browser.close()
        print("leaving early")
        return reviews

    reviews = await helpers.review_scraper.scrape_all_reviews(page)

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


async def get_summarized_reviews(place: str, city: str):
    # Model Configuration
    genai.configure(api_key=os.getenv("API_KEY"))
    model = genai.GenerativeModel("gemini-1.0-pro")
    reviews: list = await scrape_reviews(place, city)
    result = summarize_reviews(reviews, model)
    return result


def main():
    # Model Configuration
    genai.configure(api_key=os.getenv("API_KEY"))
    model = genai.GenerativeModel("gemini-1.0-pro")

    # Get User Input
    print(
        "Hello! I am a program which can be used to summarize the Google Reviews of a location. I will need the name, and the location of the place you want to visit in order to do so!"
    )
    place = input("\nWhat is the name of the place you want to visit?: ")

    city = input(
        "\nWhat city is this place located in? (You may also wish to include the country, state, province, or county to get accurate results): "
    )

    print(
        f"\nThank you! I will now generate a summarized review of {place} for you!\nPlease wait...\n"
    )
    # Scrape Reviews and Summarize
    reviews = asyncio.run(scrape_reviews(place, city))
    if not reviews:
        print("No reviews were found for this location.")
        return
    result = summarize_reviews(reviews, model)
    print(result)


if __name__ == "__main__":
    main()

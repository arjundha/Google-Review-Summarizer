from thefuzz import fuzz


async def load_browser(page, place: str, city: str):
    await page.setViewport({"width": 800, "height": 3200})

    # Use Google Maps to try and find the place of interest
    await page.goto("https://www.google.com/maps")
    await page.type("input#searchboxinput", f"{place} {city}")
    await page.keyboard.press("Enter")

    # Wait for the page to load
    await page.waitForNavigation()


async def find_first_result(page, timeout=30000):
    # See if multiple results came up, if so, we only want the first one
    try:
        await page.waitForSelector(".hfpxzc", timeout=timeout)
        await page.click(".hfpxzc")
    except:
        pass


async def get_location_title(page, timeout=30000):
    try:
        await page.waitForSelector(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1",
            timeout=timeout,
        )
        element = await page.querySelector(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1"
        )
        text = await page.evaluate("(element) => element.textContent", element)
        return text
    except:
        text = ""


def does_title_contain_location(title: str, location: str, confidence=50):
    formatted_title = title.lower().replace(" ", "")
    formatted_location = location.lower().replace(" ", "")
    if formatted_location in formatted_title:
        return True
    else:
        closeness = fuzz.ratio(formatted_title, formatted_location)
        print(closeness)
        return confidence <= closeness


async def click_reviews_tab(page, timeout=30000):
    # Wait for the Reviews tab to load
    await page.waitForSelector(".RWPxGd", timeout=timeout)
    children = await page.querySelectorAll(".hh2c6")
    # Click the Reviews tab (Sometimes, there are 4 tabs if a location sells tickets)
    if len(children) == 4:
        await page.click(".hh2c6[data-tab-index='2']")
    else:
        await page.click(".hh2c6[data-tab-index='1']")


async def scrape_all_reviews(page):
    reviews = []
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
            # If there is no "More" button, then just keep going
            pass

        # Try to get the text of a review, if the review has no text, then we pass
        try:
            # This is the class for a reviewer (.MyEned)
            await page.waitForSelector(".MyEned")
            reviwer = await element.querySelector(".MyEned")
            # Note: these review texts are in a class called .wiI7pd
            review = await element.querySelector(".wiI7pd")
            review = await page.evaluate("(element) => element.textContent", review)
            reviews.append(review)
        except:
            pass

    return reviews


if __name__ == "__main__":
    # string1 = "their bkr cafe"
    # string2 = "Purebread Bakery + Coffee"
    # print(does_title_contain_location(string1, string2))
    pass

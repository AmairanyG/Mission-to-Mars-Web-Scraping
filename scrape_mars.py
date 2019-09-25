import requests
import pandas as pd


def scrape():
    from bs4 import BeautifulSoup
    from splinter import Browser

    # Part 1

    response = requests.get("https://mars.nasa.gov/news/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text)
    else:
        print("There was an error going to your webpage")

    news_title = soup.findAll("div", {"class": "content_title"})[0].findAll("a")[0].text
    news_p = (
        soup.findAll("div", {"class": "image_and_description_container"})[0]
        .findAll("div", {"class": "rollover_description_inner"})[0]
        .text
    )

    # Part 2

    browser = Browser("chromedriver")

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    soup2 = BeautifulSoup(browser.html)

    featured_image = (
        "https://www.jpl.nasa.gov"
        + soup2.findAll("article", {"class": "carousel_item"})[0]["style"].split(
            "background-image: url('"
        )[1][:-3]
    )

    # Part 3

    response = requests.get("https://twitter.com/marswxreport?lang=en")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text)
    else:
        print("There was an error going to your webpage")

    mars_weather = soup.findAll("div", {"class": {"js-tweet-text-container"}})[0].text

    # Part 4

    res = requests.get("https://space-facts.com/mars/")
    soup = BeautifulSoup(res.content, "lxml")
    table = soup.find_all("table")[1]
    df_mars = pd.read_html(str(table))[0]

    # Part 5
    from splinter import Browser
    from bs4 import BeautifulSoup

    browser = Browser("chromedriver")

    browser.visit(
        "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )
    results = browser.find_by_css('img[class="thumb"]')
    num_tries = len(results)
    hemisphere_image_urls = []

    for trial in range(0, num_tries):
        browser.visit(
            "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        )
        results = browser.find_by_css('img[class="thumb"]')
        results[trial].click()
        soup = BeautifulSoup(browser.html)
        hemisphere_image_urls.append(
            dict(
                title=soup.find_all("h2", {"class": {"title"}})[0].text,
                img_url=soup.find_all("a", string="Original")[0]["href"],
            )
        )

    return dict(
        news_title=news_title,
        news_p=news_p,
        featured_image=featured_image,
        mars_weather=mars_weather,
        df_mars=df_mars,
        hemisphere_image_urls=hemisphere_image_urls,
    )

if __name__ == "__main__":

    scrape()
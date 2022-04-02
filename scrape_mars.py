# Importing Dependencies  (Note: A lot of this will look the same as the jupyter file, as I basically had to convert it to python)
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    exe_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **exe_path, headless=False)

    # (Scrape for the Featured Image) [This is in order of the results image provided by the homework from the top-down]
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = [i.get("src") for i in soup.find_all("img", class_="headerimage fade-in")]
    featured_image_url = url + img[0]

    # (Scrape for the Top News)
    url2 = "https://redplanetscience.com/"
    browser.visit(url2)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0]
    news_p = soup.find_all('div', class_='article_teaser_body')[0]
    top_news = news_title.text
    top_paragraph = news_p.text

    # (Scrape for the Mars' Hemispheres Images)
    url3 = "https://marshemispheres.com/"
    browser.visit(url3)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    for i in range(4):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find_all("h3")[i].get_text()
        browser.find_by_tag('h3')[i].click()
        time.sleep(3)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        image_url = soup.find("img", class_="wide-image")["src"]
        hemisphere_image_urls.append({
            "title": title,
            "img_url": "https://marshemispheres.com/" + image_url
        })
        browser.back()
        time.sleep(3)

# (This segment is mainly for saving each of them into variables so they can be used properly by the HTML code)
    title1 = hemisphere_image_urls[0]["title"]
    image1 = hemisphere_image_urls[0]["img_url"]
    
    title2 = hemisphere_image_urls[1]["title"]
    image2 = hemisphere_image_urls[1]["img_url"]

    title3 = hemisphere_image_urls[2]["title"]
    image3 = hemisphere_image_urls[2]["img_url"]

    title4 = hemisphere_image_urls[3]["title"]
    image4 = hemisphere_image_urls[3]["img_url"]

    # (Scrape for Comparison Table of Mars and Earth)
    url4 = "https://galaxyfacts-mars.com/"
    browser.visit(url4)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    table_list = soup.find_all("table", class_="table")[0]

    header = [i.text for i in table_list("th")]
    column_Mars = [i.text for i in table_list("span", class_="orange")]
    column_Earth = [i.text for i in table_list("span", class_="purple")]

    combined_data = {"Description": header, "Mars": column_Mars, "Earth": column_Earth}
    comparison_df = pd.DataFrame(combined_data)
    comparison_df.set_index("Description", inplace=True)
    comparison_df["Earth"] = comparison_df["Earth"].str.replace("\t", "")
    comparison_html = comparison_df.to_html(classes="table table-striped")

    browser.quit()

    # (Dictionary Data for MongoDB)
    final_mars_data = {
        "latest_news": top_news,
        "latest_news_p": top_paragraph,
        "featured_image": featured_image_url,
        "comparison_table": comparison_html,
        "hemisphere_images": hemisphere_image_urls,
        "title1": title1,
        "title2": title2,
        "title3": title3,
        "title4": title4,
        "image1": image1,
        "image2": image2,
        "image3": image3,
        "image4": image4,
    }
    return final_mars_data
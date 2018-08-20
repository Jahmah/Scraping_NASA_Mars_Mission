#Imports & Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd



#Site navigation
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# Defining scrape function & dictionary
def scrape():
    mars_data = {}
    output = marsNews()
    mars_data["mars_news"] = output[0]
    mars_data["mars_paragraph"] = output[1]
    mars_data["mars_image"] = marsImage()
    mars_data["mars_weather"] = marsWeather()
    mars_data["mars_facts"] = marsFacts()
    mars_data["mars_hemisphere"] = marsHem()

    return mars_data



#NASA Mars News
def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    output = [news_title, news_paragraph]
    
    return output



#JPL Mars Space Images - Featured Image
def marsImage():
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    html = browser.html
    soup = bs(html, "html.parser")
    img_url = soup.find("img", class_="thumb")["src"]
    featured_img_url = "https://www.jpl.nasa.gov" + img_url
    
    return featured_img_url


#Mars Weather
def marsWeather():
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html 
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    return mars_weather


#Mars Facts
def marsFacts():
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)
    mars_facts = pd.read_html(url_facts)
    mars_facts[0]
    df_mars_facts = mars_facts[0]
    df_mars_facts.columns = ['Parameter', 'Value']
    df_mars_facts.set_index('Parameter', inplace = True)
    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace('\n', '')
    
    return mars_html_table



# Mars Hemispheres
def marsHem():
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    html = browser.html
    soup = bs(html, "html.parser")

    url_hemisphere_images = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + link    
        browser.visit(image_link)
        html = browser.html
        soup= bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        url_hemisphere_images.append({"title": title, "img_url": image_url})

    return url_hemisphere_images


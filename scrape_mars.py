# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time 


# Create master function 'scrape_mars'

def scrape_marsInfo(mongo):

    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest 
    # News Title and Paragraph Text. Assign the text to variables that you can reference later.
    # executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", executable_path="C:/Users/Joseph/Desktop/Data_Boot_Camp/Web/Webscraping/MongoDB/Web_Scraping_HW_Instructions/Instructions/web-scraping-challenge/chromedriver.exe", headless=False)
    headline, teaser = scrape_news(browser)

    scrapedata = {
        'headline':headline,
        'teaser':teaser,
        'weather': scrape_tweet(browser),
        'featureimage': scrape_img(browser),
        'marsfacts': mars_table(),
        'pics': scrape_hemis(browser)}
    
    # Close the browser after scraping
    browser.quit()
    print(scrapedata)
    #collection = mongo.db.mars_collection
    #collection.update({}, scrapedata, upsert=True)
    mongo.db.mars_collection.replace_one({}, scrapedata, upsert=True)
    # Return results
    return scrapedata

def scrape_news(browser):

    mars_url = 'https://mars.nasa.gov/news/'

    browser.visit(mars_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    title_list = []
    p_list = []


    all_titles = soup.find_all('div', class_ = "content_title")
    all_p = soup.find_all('div', class_ = "image_and_description_container")

    mars_news = []
    for title in all_titles:
        try:
            mars_title = title.find('a').text
            print("-------------------------------------------------------------------------")
            print("mars_title")
            print(mars_title)
            print("-------------------------------------------------------------------------")
            title_list.append(mars_title)
        except AttributeError:
            title_list.append("")
    print("-------------------------------------------------------------------------")
    print("title_list")
    print(title_list)
    print("-------------------------------------------------------------------------")    
    p_list.append("")    
    
    for paragraph in all_p:
        try:
            mars_p = paragraph.find('div', class_ = "rollover_description_inner").text
            p_list.append(mars_p)
        except AttributeError:
            p_list.append("")

    print("-------------------------------------------------------------------------")
    print("len(p_list)")
    print(len(p_list))
    print("len(title_list)")
    print(len(title_list))
    print("len(title_list)")
    print(len(all_titles))
    print("-------------------------------------------------------------------------")
    

    for i in range(len(all_titles)):
        mars_news.append({"title": title_list[i], "description": p_list[i]})

    first_marsNews = mars_news[1]
    headline = first_marsNews['title']
    teaser = first_marsNews['description']

    print("-------------------------------------------------------------------------")
    print("mars_news")
    print(mars_news)
    print("-------------------------------------------------------------------------")
    print("headline")
    print(headline)
    print("teaser")
    print(teaser)
    print("-------------------------------------------------------------------------")
    return headline, teaser

    #Visit the url for JPL  Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    #Use splinter to navigate the site and find the image url for the current  Mars Image and assign the 
    #url string to a variable called `_image_url`.

    
def scrape_img(browser):

    marsImage_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(marsImage_url)

    img_button = browser.find_by_id("full_image")
    img_button.click()
    time.sleep(5)
    moreInfo_button = browser.find_by_text("more info     ")
    moreInfo_button.click()

    html = browser.html

    full_img = bs(html, "html.parser")

    full_img_link = full_img.find('figure')
    img_url = "https://www.jpl.nasa.gov" + full_img_link.a.img['src']

    print("-------------------------------------------------------------------------")
    print("img_url")
    print(img_url)
    print("-------------------------------------------------------------------------")

    return img_url


def scrape_tweet(browser):

    ##Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars
    # weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.

    marsWeather_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(marsWeather_url)
    time.sleep(5)
    html = browser.html
    tweet_soup = bs(html, 'html.parser')

    mars_weather_tweet = tweet_soup.find('div', attrs={"class": "css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"})

    #mars_weather_tweet = tweet_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    

    return mars_weather_tweet.text


def mars_table():
    
    # Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.
    import pandas as pd
    mars_df = pd.read_html('https://space-facts.com/mars/')[0]


    mars_df.columns=['description', 'value']
    mars_df.set_index('description', inplace=True)

    print("-------------------------------------------------------------------------")
    print("mars_df")
    print(mars_df)
    print("-------------------------------------------------------------------------")

    #mars_df2 = mars_df.to_dict('description')
    

    return mars_df.to_html(classes="table table-striped")

def scrape_hemis(browser):

    # Visit the USGS Astrogeology site 
    #[here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    #to obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the 
    #hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary 
    #for each hemisphere.


    marsHemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(marsHemispheres_url)
    time.sleep(3)

    hemisphere_image_urls = []

    hemisphereImagelinks = browser.find_by_css("a.product-item h3")

    for i in range(len(hemisphereImagelinks)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[i].click()
   
        sample = browser.find_link_by_text('Sample').first
    
        hemisphere['img_url'] = sample['href']
    
        # Scrape Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
    
        # Append hemisphere to hemisphere list
    
        hemisphere_image_urls.append(hemisphere)
    
        browser.back()

    return hemisphere_image_urls

"""     def scrape(browser):
        scrapedata = {}
        scrapedata['headline']=headline
        scrapedata['teaser']=teaser
        scrapedata['weather']= mars_weather_tweet.text
        scrapedata['featureimage']= img_url
        scrapedata['marsfacts']= mars_df2
        scrapedata['pics'] = hemisphere_image_urls
    

        myclient = PyMongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["scrapeMars_DB"]
        collection = mydb.mars_collection
        collection.update({}, scrapedata, upsert=True) """

# if __name__ == "__main__":
   # print(scrape_marsInfo())

#!/usr/bin/env python
# coding: utf-8


# Import Splinter, BeautifulSoup, and Pandas
import fractions
from hashlib import new
from click import style
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import time


def scrape_all():
    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    
    #run all scraping function and store results in dictinary
    scrape_results = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)     
    }

    return scrape_results


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
def mars_news(browser):
    
    #Visit the mars website 
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try except
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Begin scraping
        # slide_elem.find("div", class_= 'content_title')
        
        # use parent element to find 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_ = 'content_title').get_text()
        print(news_title)
        
        # Use parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### JPL Space Images Featured Image
def featured_image(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #print(img_soup)

    # add try /except fro error handling
    
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #print(img_url_rel)
    except AttributeError:
        return None


    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #print(img_url)
    
    return img_url

# ### Mars Facts
def mars_facts():
    # Add try/except fro error handling
    try:     
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        # df.head()
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    print(df)


    return df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        hemispheres = {}
    
        # find and click hemisphere page link
        browser.find_by_css('a.product-item img')[i].click()
        # Begin Scraping
        # look insede to full image url
        element = browser.find_link_by_text('Sample').first.click()
        # print(element)
        # print(browser.url)
        #img_link= element('herf').get('src')
    
        #look insde to h2 tag for text
        #img_title = browser.find_by_css("h2.title").text
    
        #hemispheres["img_link"] = hemisphere_image_urls
        # print(img_url)
    
        #hemispheres["img_title"] = img_title
        #print(title)
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_image_urls.append(hemispheres)
        browser.back()    
    
    return  hemisphere_image_urls

def scrape_hemisphere(html_text):
    # parse html text
    hemisphere_soup = soup(html_text, "html.parser")
    # adding try/except for error handling
    try:
        title_elem = hemisphere_soup.find("h2", class_="title").get_text()
        sample_elem = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None
    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }
    return hemispheres
    
if __name__ == "__main__":
    print(scrape_all ())
    print('test success')


# 4. Print the list that holds the dictionary of each image url and title.
#print(hemisphere_image_urls)


# 5. Quit the browser
#browser.quit()




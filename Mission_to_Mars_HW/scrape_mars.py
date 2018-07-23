
# coding: utf-8

# In[4]:


# get_ipython().system(' pip install sz')


# In[46]:


#Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
from selenium import webdriver
executable_path = {"executable_path": "/Users/DanielByrne/Desktop/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
import tweepy
from keys import (consumer_key, 
                    consumer_secret, 
                    access_token, 
                    access_token_secret)
import pandas as pd


# In[47]:


def init_browser():
    executable_path = {"executable_path": "/Users/DanielByrne/Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
 

    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the latest Mars news.
    article = soup.find("div", class_="list_text")
    article_teaser = article.find("div", class_="article_teaser_body").text
    article_title = article.find("div", class_="content_title").text
    article_date = article.find("div", class_="list_date").text
  
    # Add the news date, title and summary to the dictionary
    mars_data["news_date"] = article_date
    mars_data["news_title"] = article_title
    mars_data["summary"] = article_teaser

#Visit the JPL Mars
url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url2)


# In[51]:


#Scrape the browser into beautiful soup 
#Save the image to`img_url`
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
image = soup.find("img", class_="thumb")["src"]
img_url = "https://jpl.nasa.gov"+image
featured_image_url = img_url

# Add the featured image url to the dictionary
featured_image_url= mars_data["featured_image_url"]


# In[52]:


#Use the requests library to download and save the image 
import requests
import shutil
response = requests.get(img_url, stream=True)
with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
    
# Display the image with IPython.display
from IPython.display import Image
Image(url='img.jpg')


# In[53]:


#Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
target_user = "marswxreport"
full_tweet = api.user_timeline(target_user , count = 1)
mars_weather=full_tweet[0]['text']
mars_weather

# Add the weather to the dictionary
mars_data["mars_weather"] = mars_weather


# In[54]:


#Visit the Mars facts webpage and scrape table data into Pandas
url3 = "http://space-facts.com/mars/"
browser.visit(url3)

grab=pd.read_html(url3)
mars_info=pd.DataFrame(grab[0])
mars_info.columns=['Mars','Data']
mars_table=mars_info.set_index("Mars")
marsinformation = mars_table.to_html(classes='marsinformation')
marsinformation =marsinformation.replace('\n', ' ')

# Add the Mars facts table to the dictionary
mars_data["mars_table"] = marsinformation


# In[55]:


#Output to html after loading and cleaning in Pandas
grab=pd.read_html(url3)
mars_data=pd.DataFrame(grab[0])
mars_data.columns=['Mars','Data']
mars_table=mars_data.set_index("Mars")
marsdata = mars_table.to_html(classes='marsdata')
marsdata=marsdata.replace('\n', ' ')
marsdata


# In[56]:


#Visit the USGS Astogeology site and scrape pictures of the hemispheres
url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url4)


# In[57]:


#Use splinter to loop through the 4 images and load into dict
import time 
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
mars_hemispheres=[]





# In[59]:


url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemisphere)


# In[60]:


#Base url
from urllib.parse import urlsplit


# In[61]:


hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
hemisphere_base_url


# In[62]:


hemisphere_img_urls = []
results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
time.sleep(2)
cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
cerberus_image = browser.html
soup = bs(cerberus_image, "html.parser")
cerberus_url = soup.find("img", class_="wide-image")["src"]
cerberus_img_url = hemisphere_base_url + cerberus_url
cerberus_title = soup.find("h2",class_="title").text
backbutton = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
cerberus = {"image title":cerberus_title, "image url": cerberus_img_url}
hemisphere_img_urls.append(cerberus)

print(cerberus_img_url)
print(cerberus_title)


# In[63]:


results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
time.sleep(2)
schiaparelli_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
schiaparelli_image = browser.html
soup = bs(schiaparelli_image, "html.parser")
schiaparelli_url = soup.find("img", class_="wide-image")["src"]
schiaparelli_img_url = hemisphere_base_url + schiaparelli_url
schiaparelli_title = soup.find("h2",class_="title").text
backbutton = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_img_url}
hemisphere_img_urls.append(schiaparelli)

print(schiaparelli_img_url)
print(schiaparelli_title)


# In[64]:


results1results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
time.sleep(2)
syrtis_major_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
syrtis_major_image = browser.html
soup = bs(syrtis_major_image, "html.parser")
syrtis_major_url = soup.find("img", class_="wide-image")["src"]
syrtis_major_img_url = hemisphere_base_url + syrtis_major_url
syrtis_major_title = soup.find("h2",class_="title").text
backbutton = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_img_url}
hemisphere_img_urls.append(syrtis_major)

print(syrtis_major_title)
print(syrtis_major_img_url)


# In[65]:


results1results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
time.sleep(2)
valles_marineris_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
valles_marineris_image = browser.html
soup = bs(valles_marineris_image, "html.parser")
valles_marineris_url = soup.find("img", class_="wide-image")["src"]
valles_marineris_img_url = hemisphere_base_url + syrtis_major_url
valles_marineris_title = soup.find("h2",class_="title").text
backbutton = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_img_url}
hemisphere_img_urls.append(valles_marineris)

print(valles_marineris_img_url)
print(valles_marineris_title)


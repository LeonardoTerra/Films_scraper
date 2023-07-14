# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 20:44:35 2023

@author: leeon
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

#Email modules
import email.mime.multipart
import email.mime.text
import smtplib
import email
import email.mime.application


url = 'https://www.cinemark.com.br/'

driver = webdriver.Chrome('C:/Users/leeon/.spyder-py3/chromedriver.exe')
driver.get(url)

#Locations where Cinemark is available and city input

def location():
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    locations = []
    location_path = soup.find('div', id="citysDesktop")
    for cities in location_path:
        cities.find_all('a')
        locations.append(cities.string)
    return locations


print("Locations where Cinemark is available:", ", ".join(location()))

city = input('What city do you live: ').replace(" ", "-").lower()

city_url = 'https://www.cinemark.com.br/'+str(city)+'/filmes/em-cartaz?pagina=1'

driver.get(city_url)

sleep(3)

#Defining the variables and the dataframe
movies = []
summaries = []
ratings = []

df = pd.DataFrame()

#Executing the code:

while True:
    
    #Getting the page source from the driver a for the city and run the bot.
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    
    #Getting the number of movies in the page
    in_page = soup.find_all('h3', class_="movie-title")
    in_page

    elements = []

    for element in in_page:
        for i in element.find_all('a'):
            elements.append(i)

    n_in_page = len(elements)+1
    n_in_page
    
    movie_name = [driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div/div['+str(i)+']/article/div/a').get_attribute('title') for i in range(1,n_in_page)]
    for i in movie_name:
        movie = str(i).replace("Filme ","")
        movies.append(movie)
  
    in_page_span = soup.find_all('div',class_="movie-details")
    for i in in_page_span:
        for rating in i.find_all('span', class_="rating-abbr"):
            ratings.append(rating.string)

    summary_link = [driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div/div['+str(i)+']/article/div/div/ul/li/a').get_attribute('href') for i in range(1,n_in_page)]
    for i in summary_link:
        summary = str(i)
        summaries.append(summary)
        
    # Getting the movies from the next page if available
    try:
        next_page = soup.find('a', class_="pagination-next").get('href')
        driver.get(next_page)
    except:
        break

#Saving the data to the csv file

try:
    df = pd.DataFrame({'Movie': movies, 'Rates': ratings, 'Book': summaries})
    df.to_csv("C:/Users/leeon/Desktop/file.csv",index=False, encoding="ANSI")
except:
    print('Something wrong...')

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 20:44:35 2023

@author: leeon
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

#Choose the city one wants to see the movies in theaters

city = input('What city do you live: ').replace(" ", "-").lower()
city

#Getting the url for the city and run the bot.

url = 'https://www.cinemark.com.br/'+str(city)+'/filmes/em-cartaz?pagina=1'

driver = webdriver.Chrome('C:/Users/leeon/.spyder-py3/chromedriver.exe')
driver.get(url)

sleep(3)
#Getting the page source from the driver a for the city and run the bot.
'''
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

in_page = soup.find_all('h3', class_="movie-title")
'''
#Getting the number of movies in the page
'''
elements = []

for element in in_page:
    for i in element.find_all('a'):
        elements.append(i)

n_in_page = len(elements)
n_in_page
'''

movies = []
summaries = []
ratings = []
#To make the bot get all movies in the page and the variables (movies, rates, link)

df = pd.DataFrame()

while True:

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    in_page = soup.find_all('h3', class_="movie-title")
    in_page
    #Getting the number of movies in the page

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

    try:
        next_page = soup.find('a', class_="pagination-next").get('href')
        driver.get(next_page)
    except:
        break

movies
summaries
ratings

df = pd.DataFrame({'Movie': movies, 'Rates': ratings, 'Book': summaries})
df.to_csv("C:/Users/leeon/Desktop/file.csv",index=False, encoding="ANSI")

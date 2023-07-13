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

#Choose the city to see the movies in theaters
#Coomon cities are São Paulo, Belo Horizonte, Rio de Janeiro, Brasilia, Porto Alegre etc.

city = input('What city do you live: ').replace(" ", "-").lower()
city

url = 'https://www.cinemark.com.br/'+str(city)+'/filmes/em-cartaz?pagina=1'

driver = webdriver.Chrome('C:/Users/leeon/.spyder-py3/chromedriver.exe')
driver.get(url)

sleep(3)

#Defining the variables and the dataframe
movies = []
summaries = []
ratings = []

df = pd.DataFrame()

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
df = pd.DataFrame({'Movie': movies, 'Rates': ratings, 'Book': summaries})
df.to_csv("C:/Users/leeon/Desktop/file.csv",index=False, encoding="ANSI")

from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import sqlite3

#minutes between scraps
sleep_time = 60

#sqlite connection
conn = sqlite3.connect('items.db')
c = conn.cursor()

#c.execute('''CREATE TABLE items(date DATE, name TEXT, price TEXT)''')

#scrap search page
def scrap_search(link):
    #Getting html
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text,'lxml')

    #results
    items = soup.find_all('li', class_ = 'clear product-results__list-item')

    for item in items:
        product_name = item.find('h3', class_ = 'product-results__prod-title product-results__prod-title--full').a.span.text
        product_price = item.find('span', class_ = "product-results__final-price").text

        print(f'{product_name} - {product_price}')
        c.execute('''INSERT INTO items VALUES(?,?,?)''',(datetime.now(),product_name,product_price))

#Main function
def main():

    links = []

    #Reading file lines
    with open('links.txt','r') as f:
        links = f.readlines()

    #Striping newlines from lines
    links = [link.strip('\n') for link in links]

    #Iterating over each link
    for link in links:
        #scrap page
        scrap_search(link)

        #commit the inserts
        conn.commit()

if __name__ == '__main__':

    while True:
        print('Scraping pages...')
        main()

        print(f'Waiting {sleep_time} minutes...')
        time.sleep(sleep_time * 60)
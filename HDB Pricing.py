#import all libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import pandas as pd
from datetime import datetime

#reads in existing .csv file
try:
    df_archive = pd.read_csv('hdb-bto-prices.csv', index_col='Date')
    df_archive.index = pd.to_datetime(df_archive.index)

#if it doesn't exist, create new dataframe
except:
    df_archive = pd.DataFrame(columns=['Date', 'Town', 'Contract', 'Type', 'Price', 'Subsidised Price'])

#extract source code of main webpage that holds all past sales launch urls
url = "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/bto-sbf"
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
html_doc = driver.execute_script("return document.documentElement.innerHTML")
driver.quit()

soupMain = BeautifulSoup(html_doc, 'html.parser')
section = soupMain.find_all(class_='accordion-navigation')[1]

#append individual links to a list
pastSalesURL = []
for row in section.find_all('td'):
    for link in row.find_all('a'):
        pastSalesURL.append(link.get('href'))

#loop through list and scrape source code from each link
sourceCodes = []
for page in pastSalesURL:
    print(page)
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(page)
    res = driver.execute_script("return document.documentElement.innerHTML")
    driver.quit()
    sourceCodes.append(res)
    time.sleep(random.choice(list(range(1,4))))

df = pd.DataFrame(columns=['Date', 'Town', 'Contract', 'Type', 'Price', 'Subsidised Price'])

#extract relevant data from each Sales Launch page
for webpage in sourceCodes:
    soupPage = BeautifulSoup(webpage, 'html.parser')
    table = soupPage.find('table')
    rows = table.find_all(True, class_=['bg-lite', 'bg-dark'])
    town = ''
    contract = ''
    date = table.find('tr').text[:-13].strip('\n')

    for tr in rows:
        list = [date]
        if 'first-row' in tr.get('class'):
            town = tr.find_next('td').text
            contract = tr.find_next('td').find_next('td').text
            for td in tr.find_all('td'):
                list.append(td.text)
        else:
            list.extend([town, contract])
            for td in tr.find_all('td'):
                list.append(td.text)
        s = pd.Series(list, index=df.columns)
        df = df.append(s, ignore_index=True)

#parse data into appropriate dtype
df['Price'] = df['Price'].apply(lambda x: int(''.join(c for c in x if c.isdigit())))
df['Subsidised Price'] = df['Subsidised Price'].apply(lambda x: int(''.join(c for c in x if c.isdigit())))
df['Date'] = df['Date'].map(lambda x: datetime.strptime('01-' + ('-'.join(x.split(' '))), '%d-%B-%Y'))
df = df.set_index('Date')

#append scraped date to existing file
df_archive = df_archive.append(df)
df_archive = df_archive.drop_duplicates()
df_archive = df_archive.sort_values(['Date', 'Town'], ascending=[False, True])

#export as .csv file
df_archive.to_csv('hdb-bto-prices.csv')


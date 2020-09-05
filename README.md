# hdb-bto-webscraper
Web scraper to grab HDB BTO flat prices

Welcome to my webscraper program that extracts BTO flats price data from the hdb website https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/bto-sbf.

Problem: The BTO prices are available only on individual webpages based on their sales launch period (e.g. May 2019). The HDB website does not allow users to grab a csv version nor does it provide an API.

Solution: A webscraper that uses the BeautifulSoup and Selenium libraries to extract and parse the data into a dataframe, ultimately exporting the data into an excel file. The only hard-coded input is the main url (the aforementioned link) that contains the urls of the individual sales launches.

Pre-requisites: Run pip install -r requirements.txt on your terminal

Enjoy!

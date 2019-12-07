# stocksorted

www.stocksorted.com

Overall Design of Yahoo Finance Data Scraper - Python

1. A file with all stock tickers, company name, company sector etc. is read and stored as dictionary. 
2. 3 functions return the Yahoo Finance url of stock information page, profit and loss page, and balance sheet page. 
3. BeautifulSoup parses each of the 3 urls for the data
4. The data is then cleaned into correct format and placed into dictionary
5. The data is inserted into a MYSQL database

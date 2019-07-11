# stocksorted

Overall Design of Yahoo Finance Data Scraper - Python


1. Using BeautifulSoup grab a Yahoo Finance stock url, parse into html tree, grab headings and values and put into dictionary
2. Grab a url for the balance sheet and income statement for same stock, also parsing each url and putting heading and values into dictionaries. The dictionaries are then combined. 
3. The data is then pushed into MYSQL server. 

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 17:42:22 2019

@author: Blake
"""

from requests import get #import get function from requests module
from bs4 import BeautifulSoup #import BeautifulSoup function from bs4 module
import mysql.connector
import csv
import time
import random
from timeit import default_timer as timer


stocks = ['DXJS','ADI','AAPL','AMZN','AMAT','ADP','AVGO']

def url_grab(j):
 url = "https://finance.yahoo.com/quote/" + j + "?p" + "=" + j
 #print(url)
 return(url)

def url_grab_financials(j):
 url = "https://finance.yahoo.com/quote/" + j + "/financials?p=" + j
 #print(url)
 return(url)
 
def url_grab_balancesheet(j):
 url = "https://finance.yahoo.com/quote/" + j + "/balance-sheet?p=" + j
 #print(url)
 return(url)
 

def get_url_stockinfo(url_from_func):

 response=get(url_from_func)
 html_soup = BeautifulSoup(response.text, 'html.parser') 
 output = html_soup.find_all('tr', class_="Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px)")  
 return output
 
 
def get_url_financials(url_from_func):
 response = get(url_from_func)
 html_soup = BeautifulSoup(response.text, 'html.parser')
 output_financials = html_soup.find_all('tr', class_="Bdbw(1px) Bdbc($c-fuji-grey-c) Bdbs(s) H(36px)") 
 return output_financials


def get_url_balancesheet(url_from_func):
 response = get(url_from_func)
 html_soup = BeautifulSoup(response.text, 'html.parser')
 output_balancesheet = html_soup.find_all('tr', class_="Bdbw(1px) Bdbc($c-fuji-grey-c) Bdbs(s) H(36px)")
 return output_balancesheet






def parse_clean_financials(output):
 yo = []
 yot = []

 for tag in output:
  tdtags = tag.find_all("td")[1:2] #only grab the first figures
  for tag in tdtags:
    yo.append(tag.text)

 for tag in output:
  tdtags = tag.find_all('td')[::5] #only grab the heading
  for tag in tdtags:
    yot.append(tag.text)


 yo2 = []

 yot.remove('Revenue')
 yot.remove('Operating Expenses')
 yot.remove('Income from Continuing Operations')
 yot.remove('Non-recurring Events')
 yot.remove('Net Income') #remove all these headings that dont have figures next to them 
 del yo[0] #remove the date
 

 for i in yo:
  b = "".join(str(x) for x in i)
  c = b.replace(",","")
  d = c.replace(" ","")
 
  try: 
    yo2.append(float(d)*1000)
  except:
    yo2.append((d))

 dictionary2 = dict(zip(yot,yo2)) #combine lists and put into dictionary
 return(dictionary2)





def parse_clean(output):

 junk = [] #Initialise the output storage

 for tag in output:  #tag is the counter to iterate through the list - output
  tdtags = tag.find_all("td")
 #create new list now sorted by 'td' inside of the original sorting (nesting)
  for tag in tdtags: 
    junk.append(tag.text) #every text inside this now further sorted list is to be added the output junk



 headings = junk[::2] #new list created separating the headings from figures
 numbers = junk[1::2] #new list created separating the figures from the headings
 

 fnal = [i.strip() for i in headings] #remove any junk characters around the output obtained before
 fnalnum = [i.strip() for i in numbers] #remove any junk characters around the output obtained before
 fnalnum2 = []

 for i in fnalnum:
  b = "".join(str(x) for x in i)
  c = b.replace(",","")
  d = c.replace(" ","")

 
  try: 
    fnalnum2.append(float(d))
  except:
    fnalnum2.append((d))
  
  if "B" in fnalnum[7]:
   a = float(fnalnum[7].replace("B",""))
   e = a*1000000000 
   
  if "M" in fnalnum[7]:
   a = float(fnalnum[7].replace("M",""))
   e = a*1000000
   
 fnalnum2[7] = e 

 dictionary = dict(zip(fnal,fnalnum2)) #combine the 2 lists as key: value and put into dictionary 
 return(dictionary)
 
 
 
def parse_clean_balancesheet(output): 
 
 yin = []
 yang = []
    
 for tag in output:
  tdtags = tag.find_all("td")[1:2] #only grab the first figures
  for tag in tdtags:
   yin.append(tag.text)
    
 for tag in output:
  tdtags = tag.find_all('td')[::5] #only grab the heading
  for tag in tdtags:
   yang.append(tag.text)

    
    
 yang.remove('Current Assets')
 yang.remove('Current Liabilities')
 yang.remove("Stockholders' Equity")
 yang.remove('Period Ending')
 del yin[0]
    
 yin2 = []
    
    
 for i in yin:
  b = "".join(str(x) for x in i)
  c = b.replace(",","")
  d = c.replace(" ","")
       
  try: 
   yin2.append(float(d)*1000)
  except:
   yin2.append((d))
   
 
    
 dictionary3 = dict(zip(yang,yin2))
 return dictionary3


mydb = mysql.connector.connect(
  host="localhost",
  database="mydatabase",
  user="bdobay")


mycursor = mydb.cursor()


#mycursor.execute("CREATE TABLE stockdata (id INT AUTO_INCREMENT PRIMARY KEY, StockTicker TEXT, EntityName TEXT, Sector TEXT, Industry TEXT, PreviousClose TEXT, Open TEXT, Bid TEXT, Ask TEXT, DaysRange TEXT, 52WeekRange TEXT, Volume TEXT, MarketCap TEXT, Beta3YMONTHLY TEXT, PERatio TEXT, EPS TEXT, EarningsDate TEXT, ForwardDividendYield TEXT, ExDividendDate TEXT, TotalRevenue TEXT, CostofRevenue TEXT, ResearchDevelopment TEXT, SellingGeneralandAdministrative TEXT, NonRecurring TEXT, Others TEXT, TotalOperatingExpenses TEXT, TotalOtherIncomeExpensesNet TEXT, EarningsBeforeInterestandTaxes TEXT, InterestExpense TEXT, IncomeBeforeTax TEXT,IncomeTaxExpense TEXT, MinorityInterest TEXT, DiscontinuedOperations TEXT, ExtraordinaryItems TEXT, EffectOfAccountingChanges TEXT, NetIncome TEXT, PreferredStockAndOtherAdjustments TEXT, CashAndCashEquivalents TEXT, ShortTermInvestments TEXT, NetReceivables TEXT, Inventory TEXT, OtherCurrentAssets TEXT, TotalCurrentAssets TEXT, LongTermInvestments TEXT, PropertyPlantandEquipment TEXT, Goodwill TEXT, IntangibleAssets TEXT, AccumulatedAmortization TEXT, OtherAssets TEXT, DeferredLongTermAssetCharges TEXT, AccountsPayable TEXT, ShortCurrentLongTermDebt TEXT, OtherCurrentLiabilities TEXT, TotalCurrentLiabilities TEXT, LongTermDebt TEXT, OtherLiabilities TEXT, DeferredLongTermLiabilityCharges TEXT, NegativeGoodwill TEXT, MiscStocksOptionsWarrants TEXT, RedeemablePreferredStock TEXT, PreferredStock TEXT, CommonStock TEXT, RetainedEarnings TEXT, TreasuryStock TEXT, CapitalSurplus TEXT, OtherStockholderEquity TEXT, TotalStockholderEquity TEXT)")

with open('companylist4.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    stocks2 = []
    stocksname = []
    stockssector = []
    stocksindustry = []
    for row in csv_reader:
        stocks2.append(row["Symbol"])
        stocksname.append(row["Name"])
        stockssector.append(row["Sector"])
        stocksindustry.append(row["industry"])



        

j = 0
failedstock = []

for i in stocks2:
    x = 0
    while True and x < 3:
        x += 1
        time.sleep(random.randint(0,6))
        try:
              start = timer()
              url_to_use = url_grab(i)
              rawhtml = get_url_stockinfo(url_to_use)
              stock_info = parse_clean(rawhtml)
              print(stock_info)
              print("still working")
              url_financials = url_grab_financials(i)
              rawhtmlfinancials = get_url_financials(url_financials)
              financial_info = parse_clean_financials(rawhtmlfinancials)
              url_balancesheet = url_grab_balancesheet(i)
              rawhtmlbalancesheet = get_url_balancesheet(url_balancesheet)
              balancesheet_info = parse_clean_balancesheet(rawhtmlbalancesheet)
              print(balancesheet_info)
              dall = {}
              dall.update(stock_info)
              dall.update(financial_info)
              dall.update(balancesheet_info)
              print(dall)
              sql = "INSERT INTO stockdata (id, StockTicker, EntityName, Sector, Industry, PreviousClose, Open, Bid, Ask, DaysRange, 52WeekRange, Volume, MarketCap, Beta3YMONTHLY, PERatio, EPS, EarningsDate, ForwardDividendYield, ExDividendDate, TotalRevenue, CostofRevenue, ResearchDevelopment, SellingGeneralandAdministrative, NonRecurring, Others, TotalOperatingExpenses, TotalOtherIncomeExpensesNet, EarningsBeforeInterestandTaxes, InterestExpense, IncomeBeforeTax, IncomeTaxExpense, MinorityInterest, DiscontinuedOperations, ExtraordinaryItems, EffectOfAccountingChanges, NetIncome, PreferredStockAndOtherAdjustments, CashAndCashEquivalents, ShortTermInvestments, NetReceivables, Inventory, OtherCurrentAssets, TotalCurrentAssets, LongTermInvestments, PropertyPlantandEquipment, Goodwill, IntangibleAssets, AccumulatedAmortization, OtherAssets, DeferredLongTermAssetCharges, AccountsPayable, ShortCurrentLongTermDebt, OtherCurrentLiabilities, TotalCurrentLiabilities, LongTermDebt, OtherLiabilities, DeferredLongTermLiabilityCharges, NegativeGoodwill, MiscStocksOptionsWarrants, RedeemablePreferredStock, PreferredStock, CommonStock, RetainedEarnings, TreasuryStock, CapitalSurplus, OtherStockholderEquity, TotalStockholderEquity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
              val = list(dall.values())
              val.insert(0,0)
              val.insert(1,stocks2[j])
              val.insert(2,stocksname[j])
              val.insert(3,stockssector[j])
              val.insert(4,stocksindustry[j])             
              try: 
                  mycursor.execute(sql, val)
                  mydb.commit()
                  print("Succesfully inserted data for " + i)
                  break
              except: 
                print("Error sending data for " + i)
        except:
              failedstock.append(i)
    j += 1  


mycursor.close()
mydb.close()
print(failedstock)
print("connection ended successfully")









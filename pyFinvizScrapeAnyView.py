import requests
from bs4 import BeautifulSoup
import csv
import pdb
import datetime
#pdb.set_trace() - python step by step debugger command
print (datetime.datetime.now())
print ("Finviz Overview Start")

url = "http://finviz.com/screener.ashx?v=152&f=sh_avgvol_o200,sh_price_o2&o=recom&c=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69"
# url = "http://finviz.com/screener.ashx?v=151&f=ind_independentoilgas,sh_avgvol_o200,sh_price_o2&o=recom"
# cols = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69"
# url = "http://www.finviz.com/screener.ashx?v=151&f=ind_foreignutilities,sh_avgvol_o200,sh_price_o2&c=" + cols


response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "html.parser")
firstcount = soup.find_all('option')
lastnum = len(firstcount) - 1
lastpagenum = firstcount[lastnum].attrs['value']
currentpage = int(lastpagenum)

all_data = []
page_data = []

titleslist = soup.find_all('td',{"class" : "table-top"})

titleslisttickerid = soup.find_all('td',{"class" : "table-top-s"})
titleticker = titleslisttickerid[0].text
titlesarray = []
for title in titleslist:
    titlesarray.append(title.text)

titlesarray.insert(1,titleticker)
i = 0

while(currentpage > 0):
    i += 1
    print (str(i) + " page(s) done")
    secondurl = url + "&r=" + str(currentpage)
    secondresponse = requests.get(secondurl)
    secondhtml = secondresponse.content
    secondsoup = BeautifulSoup(secondhtml, "html.parser")
    stockdata = secondsoup.find_all('a', {"class" : "screener-link"})
    stockticker = secondsoup.find_all('a', {"class" : "screener-link-primary"})
    datalength = len(stockdata)
    total_tickers = len(stockticker)
    columns_per_row = datalength / total_tickers
    print(datalength)
    print(total_tickers)
    print(columns_per_row)

    ticker_index = 0
    while(ticker_index <= total_tickers):
        data_range = stockdata[(int)(ticker_index * columns_per_row) : (int)((ticker_index+1) * columns_per_row)]
        page_data = list(map(lambda x:x.text, data_range))
        page_data.insert(1, stockticker[total_tickers-1].text)
        all_data.append(page_data)
        page_data = []
        datalength -= columns_per_row
        total_tickers -= 1
        ticker_index += 1;
    currentpage -= 20

with open('stockoverview.csv', 'w', encoding='utf8') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=titlesarray)
    writer.writeheader()

    for data_item in all_data:
        csv_row_data = {}
        column_index = 0
        while(column_index < len(data_item)):
            csv_row_data[titlesarray[column_index]] = data_item[column_index]
            column_index += 1 
        
        writer.writerow(csv_row_data)

print (datetime.datetime.now())
print ("Finviz Overview Completed")

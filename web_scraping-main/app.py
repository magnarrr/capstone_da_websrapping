from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')

row = table.find_all('th', attrs={'class':'font-semibold text-center'})
row_length = len(row)
row_length

row2 = table.find_all('td', attrs={'class':'text-center'})
row_length2 = len(row2)
row_length2

date = []
market_cap = []
volume = []
open = []
close = []

#get Date
for i in range(0, row_length):
    Date = table.find_all('th', attrs={'class':'font-semibold text-center'})[i].text
    date.append(Date)

#get Market Cap    
for i in range(0, row_length2,4):
    Market_cap = table.find_all('td', attrs={'class':'text-center'})[i].text
    Market_cap = Market_cap.strip()
    market_cap.append(Market_cap)

#get Volume    
for i in range(1, row_length2,4):
    Volume = table.find_all('td', attrs={'class':'text-center'})[i].text
    Volume = Volume.strip()
    volume.append(Volume)

#get Open
for i in range(2, row_length2,4):
    opeen = table.find_all('td', attrs={'class':'text-center'})[i].text
    opeen = opeen.strip()
    open.append(opeen)

#get close
for i in range(3, row_length2,4):
    closee = table.find_all('td', attrs={'class':'text-center'})[i].text
    closee = closee.strip()
    close.append(closee)

#making columns

table_2 = soup.find('div', attrs={'class':'card-block'})
print(table.prettify()[:500])

columns = [th.text for th in table_2.find('thead').find_all('th')]

#change data to dataframe

df = pd.DataFrame({
    columns[0]:date,
    columns[1]:market_cap,
    columns[2]:volume,
    columns[3]:open,
    columns[4]:close
})
df.head()

#insert data wrangling here

datevolume = df[['Date','Volume']]

def delete_dollar(x):
    for i in x:
        xx = i.split('$')
        return int(xx[1].replace(',',''))

datevolume['Volume'] = datevolume[['Volume']].apply(delete_dollar, axis=1) 

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{datevolume["Volume"]}' #be careful with the " and ' 

	# generate plot
	ax = datevolume.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
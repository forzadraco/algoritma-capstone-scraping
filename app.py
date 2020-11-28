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
link = 'https://www.exchange-rates.org/history/IDR/USD/T'
url_get = requests.get(link)
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('div',attrs={'id':'ctl00_M_pnlText'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here
	row = table.find_all('tr')[i]

    #get tanggal
	tanggal = row.find_all('td')[0].text
	tanggal = tanggal.strip() #for removing the excess whitespace

	#get harga harian
	harga_harian = row.find_all('a')[0].text
	harga_harian = harga_harian.strip()
	temp.append( (tanggal, harga_harian) )

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('tanggal','harga_harian'))
#insert data wrangling here

df['harga_harian'] = df['harga_harian'].replace('[^\d.]+','',regex=True)
df['harga_harian'] = df['harga_harian'].astype('float64')

pl=df.set_index('tanggal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {round(df["harga_harian"].mean())}'

	# generate plot
	ax = pl.plot(figsize = (20,9))
	
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

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
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
results = soup.find('div', attrs={'class':'lister-list'})
#___ = ____.find_all('___')

row_length = len(results)/2

temp = [] #initiating a list 

for i in range(1, 50):
#insert the scrapping process here
    title = results.find_all('h3', class_='lister-item-header')[i].get_text().replace('\n', "").strip(" ")
    ratings = results.find_all('div', class_='inline-block ratings-imdb-rating')[i].get_text().replace('\n', "").strip(" ")
    try :
        metascore = results.find_all('span', class_='metascore favorable')[i].get_text().replace('\n', "").strip(" ")
    except :
        metascore = 'n/a'
    cond = results.find_all('span', attrs={'name':'nv'})[i].get_text().replace('\n', "").strip(" ")
    if(cond.startswith('$') == False):
        votes = cond
    temp.append((title,ratings,metascore,votes))
    
temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('title','ratings', 'metascore','votes'))

#insert data wrangling here
data.ratings = data.ratings.astype('float64')
data.votes = data.votes.str.replace(",","")
data.votes = data.votes.astype('int')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["votes"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = card_data.plot(figsize = (20,9)) 
	
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
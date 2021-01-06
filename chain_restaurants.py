import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd

# Store all chain restaurants
chain_restaurants = []
# Store the result from BeautifulSoup
result = []

# Set the url
url_1 = 'https://en.wikipedia.org/wiki/List_of_Canadian_restaurant_chains'
url_2 = 'https://en.wikipedia.org/wiki/List_of_restaurant_chains'

response = requests.get(url_1)

# # Parse the html with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Get all the name with class "mw-headline"
for restaurant in soup.findAll("span", {"class": "mw-headline"}):
	result.append(restaurant.get_text())

# The first and the last three are not names of restaurants
result = result[1:-3]

# Delete '( )' from names since in OSM there is no '()'
for restaurant in result:
	name = restaurant.split(' (')
	chain_restaurants.append(name[0])


# Get data from the second url
response = requests.get(url_2)

# Parse the html with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

contentTable = soup.find("table", {"class": "wikitable sortable"})
# Get all the name with class "mw-headline"
for restaurant in contentTable.findAll("tr"):
	name = restaurant.find('a', href=True, title=True)
	if name is not None:
		chain_restaurants.append(name.get_text())

# Sort and remove duplicates
chain_restaurants.sort()
chain_restaurants = list(dict.fromkeys(chain_restaurants))


# Save the result
pd_chain = pd.DataFrame(chain_restaurants)
pd_chain.to_csv('chain_restaurants.csv', index=False, header=False)
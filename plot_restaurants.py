import pandas as pd
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import seaborn
seaborn.set()

data = 'osm/amenities-vancouver.json.gz'
chain_file = 'chain_restaurants.csv'
# Read the OSM data
amenities = pd.read_json(data, lines=True)
# Read the map of Greater Vancouver
vancouver = mpimg.imread("image/bigmap.png")
# Read the list of chain restaurants
chain_restaurants = pd.read_csv(chain_file, names=['name'])
chain_restaurants = chain_restaurants['name'].tolist()

# If the restaurant in the list of chain restaurants
def is_chain(name):
	return name in chain_restaurants

# Convert longitude and latitude to coordinates
def convert_lon_lat(df):
	# Get the height and width of the image
	height = vancouver.shape[0]
	width = vancouver.shape[1]
	unit_lon = width / (-122 +123.5)
	unit_lat = height / 0.5
	x = (df['lon'].values + 123.5) * unit_lon
	y = (49.5 - df['lat'].values) * unit_lat 
	return x, y

# Seperate chain and non-chain
def sep_restaurants(amenities):
	# Select all restaurants
	all_restaurants = amenities[(amenities['amenity'] == 'cafe') | 
				(amenities['amenity'] == 'restaurant') | 
				(amenities['amenity'] == 'fast_food')]
	# Get all restaurants that is in the list of chain restaurants
	chain = all_restaurants[all_restaurants['name'].apply(is_chain)]
	# Get all restaurants that is not in the list of chain restaurants
	non_chain = all_restaurants[~all_restaurants['name'].apply(is_chain)]
	return chain, non_chain



if __name__ == "__main__":
	# Seperate chain and non-chain
	chain, non_chain = sep_restaurants(amenities)

	# Convert longitude and latitude to coordinates
	x_chain, y_chain = convert_lon_lat(chain)
	x_non_chain, y_non_chain = convert_lon_lat(non_chain)

	# Plot chain and non-chain restaurants
	plt.imshow(vancouver)
	plt.title("Locations of chain/non-chain restaurants in Greater Vancouver")
	nc = plt.scatter(x_non_chain, y_non_chain, marker=".", color="blue", s=15)
	c = plt.scatter(x_chain, y_chain, marker=".", color="red", s=15)
	plt.legend((nc, c), ('non-chain', 'chain'))
	plt.show()

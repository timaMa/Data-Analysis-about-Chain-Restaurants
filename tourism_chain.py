import pandas as pd
import numpy as np
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy import stats

from plot_restaurants import sep_restaurants
from plot_restaurants import convert_lon_lat

import seaborn
seaborn.set()

# Read all needed data
data = 'osm/amenities-vancouver.json.gz'
chain_file = 'chain_restaurants.csv'
# Read the OSM data
amenities = pd.read_json(data, lines=True)
# Read the map of Greater Vancouver
vancouver = mpimg.imread("image/bigmap.png")
# Read the list of chain restaurants
chain_restaurants = pd.read_csv(chain_file, names=['name'])
chain_restaurants = chain_restaurants['name'].tolist()

# Degree change pre mile 
deg_lat_permile = 1/69
deg_lon_permile = 1/55

# Check if tags contain 'tourism'
def has_tourism(tags):
	return 'tourism' in tags

# Get amenities with tag 'tourism'
def get_toursim():
	return amenities[amenities['tags'].apply(has_tourism)]

# Get the number of chain restaurants within x mile(s)
def check_tourism(lat_lon, tourism, x):
	lat = lat_lon[0]
	lon = lat_lon[1]
	lat_max = lat + x * deg_lat_permile
	lat_min = lat - x * deg_lat_permile
	lon_max = lon + x * deg_lon_permile
	lon_min = lon - x * deg_lon_permile
	df_tourism = tourism[(tourism['lat'] <= lat_max) & 
					(tourism['lat'] >= lat_min) & 
					(tourism['lon'] <= lon_max) & 
					(tourism['lon'] >= lon_min) ]
	return not df_tourism.empty

if __name__ == "__main__":
 	# Seperate chain and non-chain
	chain, non_chain = sep_restaurants(amenities)
	
	# Get amenities with tag 'tourism'
	tourism = get_toursim()

	# There is at least one tourism within one mile for the chain restaurant
	chain['lat_lon'] = chain[['lat', 'lon']].values.tolist()
	chain['has_tourism'] = chain['lat_lon'].apply(check_tourism, args=(tourism, 1))

	# Group by 'has_tourism' to figure out how many chain restaurants are around toursim
	tourism_chain = chain.groupby(by='has_tourism').count()
	
	# Do the same to non-chain restaurants
	non_chain['lat_lon'] = non_chain[['lat', 'lon']].values.tolist()
	non_chain['has_tourism'] = non_chain['lat_lon'].apply(check_tourism, args=(tourism, 1))

	# Group by 'has_tourism' to figure out how many chain restaurants are around tourism
	tourism_non_chain = non_chain.groupby(by='has_tourism').count()
	contingency = [[tourism_chain['lat_lon'].values[1], tourism_non_chain['lat_lon'].values[1]], 
					[tourism_chain['lat_lon'].values[0], tourism_non_chain['lat_lon'].values[0]]]
	chi2, p, dof, expected = stats.chi2_contingency(contingency)
	# Print p-value
	print("pvalue: ", p)
	print("Percentage of chain restaurants near tourism: ", contingency[0][0] / (contingency[0][0] + contingency[0][1]))
	print("Percentage of chain restaurants far from tourism: ", contingency[1][0] / (contingency[1][0] + contingency[1][1]))
	
	xlabels = ['With tourism nearby', 'Without tourism nearby']
	num_chain = [contingency[0][0], contingency[1][0]]
	num_non_chain = [contingency[0][1], contingency[1][1]]
	plt.title('Number of chain/non-chain restaurants near/far from tourism')
	plt.bar(xlabels, num_non_chain,  width=0.5, label='Non-chain restaurants', fc='g')
	plt.bar(xlabels, num_chain, bottom=num_non_chain, width=0.5, label='Chain restaurants',fc='r')
	plt.legend()
	plt.show()


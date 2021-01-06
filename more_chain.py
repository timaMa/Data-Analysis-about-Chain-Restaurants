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

# Calculate the number of chain restaurants that in the range of [min, max]
def cal_near(value, chain, dim):
	if dim == 'lat':
		minimum = value - deg_lat_permile
		maximum = value + deg_lat_permile
	elif dim == 'lon':
		minimum = value - deg_lon_permile
		maximum = value + deg_lon_permile
	# Get chain restaurants that in the range
	df_chain = chain[(chain[dim] <= maximum) & (chain[dim] >= minimum)]
	return df_chain.count()[0]

# Calculate the number of chain restaurants near the current latitude (within 1 mile)
def cal_num(chain):
	chain['num_lat'] = chain['lat'].apply(cal_near, args=(chain, 'lat'))
	chain['num_lon'] = chain['lon'].apply(cal_near, args=(chain, 'lon'))
	return chain

if __name__ == "__main__":
 	# Seperate chain and non-chain
	chain, non_chain = sep_restaurants(amenities)
	
	num_chain = cal_num(chain)
	sort_lat = num_chain.sort_values(by='lat')
	sort_lon = num_chain.sort_values(by='lon')
	reg_lat = stats.linregress(sort_lat['lat'].values, sort_lat['num_lat'].values)
	reg_lon = stats.linregress(sort_lon['lon'].values, sort_lon['num_lon'].values)
	# Print the pvalue of linear regression
	print("pvalue of fit line for latitude: ", reg_lat.pvalue)
	print("pvalue of fit line for longitude: ", reg_lon.pvalue)


	plt.figure(1)
	plt.title('The number of chain restaurants near the latitude (within 1 mile)')
	plt.xlabel('Latitude')
	plt.ylabel('The number of chain restaurants')
	plt.plot(sort_lat['lat'].values, sort_lat['num_lat'].values)
	plt.plot(sort_lat['lat'].values, reg_lat.slope * sort_lat['lat'].values + reg_lat.intercept)

	plt.figure(2)
	plt.title('The number of chain restaurants near the longitude (within 1 mile)')
	plt.xlabel('Longitude')
	plt.ylabel('The number of chain restaurants')
	plt.plot(sort_lon['lon'].values, sort_lon['num_lon'].values)
	plt.plot(sort_lon['lon'].values, reg_lon.slope * sort_lon['lon'].values + reg_lon.intercept)
	plt.show()
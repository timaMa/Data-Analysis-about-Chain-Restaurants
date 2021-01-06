import pandas as pd
import numpy as np
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from plot_restaurants import sep_restaurants
from plot_restaurants import convert_lon_lat

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

amenities['lat_lon'] = amenities[['lat', 'lon']].values.tolist()

# Get the number of chain restaurants within 1 mile(s)
def cal_num(lat_lon, chain):
	lat = lat_lon[0]
	lon = lat_lon[1]
	lat_max = lat + deg_lat_permile
	lat_min = lat - deg_lat_permile
	lon_max = lon + deg_lon_permile
	lon_min = lon - deg_lon_permile
	df_chain = chain[(chain['lat'] <= lat_max) & 
					(chain['lat'] >= lat_min) & 
					(chain['lon'] <= lon_max) & 
					(chain['lon'] >= lon_min) ]
	return df_chain.count()[0]

# For every type of amenity calculate the number of chain restaurants for each amenity
def amenity_num(amenity_name, chain):
	amenity = amenities[amenities['amenity'] == amenity_name]
	amenity['num_chain'] = amenity['lat_lon'].apply(cal_num, args=(chain,))
	return amenity[['amenity', 'num_chain']]

def is_satisfy(name, amenity_list):
    return name in amenity_list

if __name__ == "__main__":
 	# Seperate chain and non-chain
	chain, non_chain = sep_restaurants(amenities)
	
	not_restaurants = amenities[(amenities['amenity'] != 'cafe') & 
						(amenities['amenity'] != 'restaurant') & 
						(amenities['amenity'] != 'fast_food')]

	# Get the amenity names that there are more than 40 amenities for each type
	satisfied_amenity = not_restaurants.groupby('amenity').count().reset_index()
	satisfied_amenity = satisfied_amenity[satisfied_amenity['lat']>40]
	amenity_names = satisfied_amenity['amenity'].values

	amenity_chain = pd.DataFrame(columns=['amenity', 'num_chain'])
	# For every amenities calculate the average number of chain restaurants around it
	for names in amenity_names:
		df = amenity_num(names, chain)
		amenity_chain = pd.concat([amenity_chain, df])

	posthoc = pairwise_tukeyhsd(
	    amenity_chain['num_chain'].astype('float'), amenity_chain['amenity'],
	    alpha=0.05)
	

	df_posthoc = pd.DataFrame(data=posthoc._results_table.data[1:], columns=posthoc._results_table.data[0])
	
	results_1 = df_posthoc.groupby(['group1', 'reject']).count().reset_index()
	results_1 = results_1.pivot(index='group1', columns='reject', values='group2')

	results_2 = df_posthoc.groupby(['group2', 'reject']).count().reset_index()
	results_2 = results_2.pivot(index='group2', columns='reject', values='group1')

	results = results_1.join(results_2, lsuffix='_left').fillna(0)
	results.rename_axis("amenity", axis='index', inplace=True)
	results['False'] = results['False_left'] + results['False']
	results['True'] = results['True_left'] + results['True']
	results = results.iloc[:, [2, 3]]
	results['true_percentage'] = results.iloc[:, 1] / (results.iloc[:, 0] + results.iloc[:, 1])
	# results = results[results['true_percentage'] != 0]
	results = results.sort_values(by='true_percentage', ascending=False)
	results.to_csv('posthoc.csv')
	print(posthoc)
	fig = posthoc.plot_simultaneous()
	print(results)
	plt.show()

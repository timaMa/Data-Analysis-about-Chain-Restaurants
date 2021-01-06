# CMPT 353 Project: Analysis of chain restaurants in Greater Vancouver

## Introduction


This project is based on the data from OpenStreetMap and Wikipedia. OSM data contains the latitude and longitude
of buildings and their tags. In this project, we will do some analysis of chain restaurants and other amenities in Greater Vancouver.


### The problems we are going to address:
1. Plot chain restaurants and non-chain restaurants on the map to visualize the density of restaurants.
2. Whether some parts of Greater Vancouver have more chain restaurants?
3. Do amenities related to tourism attract chain restaurants?
4. Are there some amenities that affect the number of chain restaurants?

## Installation

```
git clone https://csil-git1.cs.surrey.sfu.ca/ywa281/cmpt-353-project.git
```

## Required libraries
```
pandas
matplotlib
seaborn
requests
urllib
bs4
numpy
scipy
statsmodels
```
## Usage
**Please do not move the locations of files since we implement the path of file in the scripts.**<br />
Each python program can run separately. There is no specific order to run. The list of chain restaurants has been provided (chain_restaurants.csv).
If chain_restaurants.csv is not in the file, then chain_restaurants.py needs to be run first to produce chain_restaurants for other programs.
```
python3 <program name>
```
Example:
```
python3 plot_restaurants.py
```
## Explanation for each file
### **Folder**
#### image
Store the map of Greater Vancouver. Use the image in plot_restaurants.py.
#### osm
The provided data contains the code for producing amenities data and amenities data.
#### results
The folder "results" contains all figures that the program produces and "49.27, -123.12.png", which is used in report but is not produced by any program. 

### **Python scripts**
#### chain_restaurants.py
Web scraper for collecting lists of chain restaurants. Running this program will produce a .csv file containing 
the list of chain restaurants, named "chain_restaurants.csv" (which already exists). If "chain_restaurants.csv" does not exist,
this program needs to be run first to produce the file, otherwise, other programs can not run properly.
#### plot_restaurants.py
This program is designed for Problem 1 and produces "plot_restaurants.png" in the folder "results". This program plots chain and non-chain restaurants on the map of Greater Vancouver. Running this program will display a plot with red and blue
points on the map of Greater Vancouver. (Red for chain, blue for non-chain)
#### more_chain.py
This program is designed for Problem 2 and produces "more_chain_lat.png" and "more_chain_lon.png" in the folder "results". Running this program will print two p-values of linear regression and display two plots including the data and fit lines.
#### tourism_chain.py
This program is designed for Problem 3 and produces "tourism_chain.png" in the folder "results". Running this program will print the p-value of Chi-Square and two percentages about the fractions of chain restaurants. 
It will also display a histogram about the number of chain/non-chain restaurants.
#### determined_factors.py
This program is designed for Problem 4 and produces "posthoc.png" in the folder "results" and "posthoc.csv". Running this program will print the the result of Post Hoc and the result that 
indicates the percentage of rejections (about the null hypothesis).

### **CSV files**
#### chain_restaurants.csv
Produced by "chain_restaurants.py". This file contains the list of chain restaurants.
#### posthoc.csv
Produced by "determined_factors.py". This file contains the types of amenities, the number of rejections, the number of failed rejections, and the percentage of rejections (about the null hypothesis).

### **PDF file**
#### CMPT_353_PROJECT.pdf
Report for this project.



import numpy as np
import pandas as pd
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=True)  # set simple_zipcode=False to use rich info database


def zip2latlon(zip):  # returns latitude and longitude of a list of zip codes
    lat = [search.by_zipcode(x).to_dict()['lat'] for x in zip]
    lon = [search.by_zipcode(x).to_dict()['lng'] for x in zip]
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    return(lat, lon)


def ltctype(df):  # determines predominant type of bed at each LTC facility
    df1 = df[['SNF', 'NF', 'SNF / NF', 'NCC', 'RES']]
    type = np.asarray(df1.idxmax(axis=1))
    return(type)


# read csv data and extract zip codes and number of beds
df = pd.read_csv('ltc_facilities.csv')
cities = df['City'].values
zip = [city[-5:] for city in cities]
beds = np.asarray(df['Bed Capacity'])
# determine type of LTC and color code
type = ltctype(df)
color = np.where(type == 'SNF', 'limegreen', np.where(type == 'NF', 'magenta', np.where(
    type == 'SNF / NF', 'dodgerblue', np.where(type == 'NCC', 'k', 'firebrick'))))
# retrieve lat and lon
[lat, lon] = zip2latlon(zip)
# makes plot and projection of indiana from cartopy
reader = shpreader.Reader('countyl010g.shp')
counties = list(reader.geometries())
COUNTIES = cfeat.ShapelyFeature(counties, ccrs.PlateCarree())
plt.figure(figsize=(8, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
size = [100*n/max(beds) for n in beds]  # scale marker size according to number of beds
ax.scatter(lon, lat, c=color, zorder=80, s=size, edgecolors='none')
# adds cartopy background features
ax.add_feature(cfeat.LAND)
ax.add_feature(cfeat.LAKES, alpha=.5)
ax.add_feature(cfeat.STATES.with_scale('50m'), linestyle='-')
ax.add_feature(COUNTIES, facecolor='none', edgecolor='gray')
# sets axes scale for IN
ax.set_extent([-88.12, -84.5, 37.4, 42])
# formatting
ax.set_title("Type and Number of Beds of Indiana LTC Facilities")
# ax.plot(-86.15, 39.768, 'r*', markersize=10, zorder=100)  # plot indianpolis
snf = mpatches.Patch(color='limegreen', label='Skilled Nursing Facility')
nf = mpatches.Patch(color='magenta', label='Nursing Facility')
snfnf = mpatches.Patch(color='dodgerblue', label='SNF / NF')
ncc = mpatches.Patch(color='k', label='Non-Certified Comprehensive')
res = mpatches.Patch(color='firebrick', label='Residential')
plt.legend(handles=[snf, nf, snfnf, ncc, res], prop={'size': 7})
plt.savefig('map.png')
plt.show()
plt.close()

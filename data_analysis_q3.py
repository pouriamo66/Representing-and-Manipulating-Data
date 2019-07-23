# Georgios Koliopoulos (2646502)

# Import libraries

import pandas as pd
import numpy as np
import seaborn as sbn
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import collections as col
import geopandas as gpd
from descartes import PolygonPatch

# Import dataset

gens = pd.read_csv('/generators.csv')

# Delete the first empty column

gens.drop(gens.columns[[0]], 1, inplace=True)
gens.head()

# Select the columns that we will work with

df = gens[['generator_name', 'country', 'ic_kw', 'technology',
          'accreditation']].copy()
df.head()

# Replace 'Photovoltaic' with 'Solar' to match the other datasets

df.technology = df.technology.replace(to_replace='Photovoltaic',
        value='Solar')

# Checking for missing values

df.isnull().any()

# Deleting rows with missing values

df = df.dropna()

# Check again for missing values

df.isnull().any()

# Create new column with Accreditation year

df['accreditation'] = pd.to_datetime(df['accreditation'],
        format='%Y-%m-%d')
accr_year = df.accreditation.dt.year
df['accr_year'] = accr_year


# Function to find the total installed capacity in GWh for any column

def capacities(column):
    column_values = column.unique()
    capacity_per_column = {}
    for value in column_values:
        capacity = df[column == value].ic_kw.sum()
        capacity_per_column[value] = capacity / 1000000
    return capacity_per_column
    print capacity_per_column


# Total capacity per country

capacities(df.country)

# Capacity per Country Bar Plot

capacity_per_technology = capacities(df.technology)
capacity_per_country = \
    col.OrderedDict(sorted(capacities(df.country).items(),
                    key=lambda t: t[1]))
(f, ax) = plt.subplots(figsize=(7, 5), sharex=True)
sbn.barplot(x=list(capacity_per_country.keys()),
            y=list(capacity_per_country.values()), palette='pastel',
            ax=ax)
ax.axhline(0, color='k', clip_on=False)
ax.set_ylabel('Installed Capacity in GWh')
ax.set_xlabel('UK countries')

# ax.set_title("Capacity of Renewable Generators per UK country")

plt.savefig('plots/cap_country.jpg')

# Merge Technologies of less than 1GWh capacity to "Other"

other = 0
to_be_deleted = []
for technology in capacity_per_technology:
    if capacity_per_technology[technology] < 1:
        other += capacity_per_technology[technology]
        to_be_deleted.append(technology)
capacity_per_technology.update({'Other': other})
print to_be_deleted
for k in to_be_deleted:
    del capacity_per_technology[k]
print capacity_per_technology

# Capacity per Technology Bar Plot

capacity_per_technology = \
    col.OrderedDict(sorted(capacity_per_technology.items(),
                    key=lambda t: t[1]))
(f, ax) = plt.subplots(figsize=(12, 6), sharex=True)
sbn.barplot(x=list(capacity_per_technology.keys()),
            y=list(capacity_per_technology.values()), palette='pastel',
            ax=ax)
ax.axhline(0, color='k', clip_on=False)
ax.set_ylabel('Installed Capacity in GWh')
ax.set_xlabel('Technology')

# ax.set_title("Capacity of Renewable Generators per technology")

plt.savefig('plots/cap_tech.jpg')

# Capacity of Technologies per country Plot

df['ic_gw'] = df.ic_kw / 1000000
cap_country_tech = df.groupby(['country', 'technology'])['ic_gw'
        ].sum().unstack()
cap_country_tech.plot(kind='bar', stacked=True, figsize=[10, 6],
                      colormap='Paired')
plt.ylabel('Installed Capacity in GWh')
plt.xlabel('UK Country')

# plt.title("Capacity of technologies in each country")

plt.xticks(rotation='horizontal')
plt.legend(title='Technology')
plt.savefig('plots/cap_country_tech')

# Time Series Plot for capacity per technology for each country

countries = df.country.unique()
for country in countries:
    country_df = df[df.country == country]
    cap_by_year = country_df.groupby(['accr_year', 'technology'
            ])['ic_gw'].sum()
    cap_by_year.unstack().plot(kind='line', figsize=[10, 7],
                               colormap='Paired')
    plt.ylabel('Installed Capacity in GWh')
    plt.xlabel('Year')

    # plt.title("Time Series Plot of installed capacity in " + country)

    plt.legend(title='Technology', bbox_to_anchor=(1.04, 1),
               loc='upper left')
    plt.savefig('plots/time_' + country, bbox_inches='tight')

# Import Shape of UK (source: https://data.gov.uk/dataset/b97c7f38-607c-4e1c-bdf1-db08b55b7566/countries-december-2017-full-extent-boundaries-in-uk)

fp = \
    '/Users/georgekoliopoulos/Desktop/Countries_December_2017_Full_Extent_Boundaries_in_UK/Countries_December_2017_Full_Extent_Boundaries_in_UK.shp'
map_df = gpd.read_file(fp)
map_df.ctry17nm.replace(to_replace='Northern Ireland', value='NI',
                        inplace=True)
map_df['total_capacity'] = map_df['ctry17nm'
                                  ].map(capacities(df.country))
map_df.head()

# Map of the UK with installed capacity per country

map = map_df.plot(column='total_capacity', figsize=(20, 10),
                  cmap='Oranges', legend=True)
map.axis('off')

# plt.title('Total Installed Capacity in GWh per country')

plt.savefig('plots/map')

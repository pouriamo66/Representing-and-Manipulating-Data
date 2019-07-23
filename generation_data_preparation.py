#!/usr/bin/env python

# Simone Fisicaro (2641824)

# import libraries
import pandas as pd


# read data from the source folder
input_data = pd.read_csv("../data/fuel_used_in_electricity_generation_and_electricity_supplied.txt", delimiter="\t", decimal=',')

# transpose and create year and quarter columns
data = input_data.set_index('index').T
data['date'] = data.index
data = data.reset_index()
data['year'] = pd.to_numeric(data.date.str.split('-').str[0])
data['quarter'] = pd.to_numeric(data.date.str.split('-').str[1])
data = data.drop(columns=['index'])

# filter data >= 2010
data_filtered = data[data.year >= 2010]
data_filtered = data_filtered.reset_index()
data_filtered = data_filtered.drop(columns=['index'])

# create on-shore columns
data_filtered['generated_wind_solar_onshore'] = data_filtered['generated_wind_solar'] - data_filtered['generated_of_which_offshore']

# create renewable and non-renewable columns
data_filtered['generated_non_renewable'] = data_filtered['generated_total'] - \
    data_filtered['generated_hydro'] - \
    data_filtered['generated_wind_solar'] - \
    data_filtered['generated_bioenergy']

data_filtered['generated_renewable'] = data_filtered['generated_total'] - data_filtered['generated_non_renewable']

# select columns
data_final = data_filtered[['year', 'quarter', 'generated_coal', 'generated_oil', 'generated_gas', 'generated_nuclear', 'generated_hydro', 'generated_wind_solar', 'generated_wind_solar_onshore', 'generated_of_which_offshore', 'generated_bioenergy', 'generated_pumped_storage', 'generated_other_fuels', 'generated_renewable', 'generated_non_renewable', 'generated_total']]


# save dataframe
data_final.to_csv('../data/generation.csv', index=False)

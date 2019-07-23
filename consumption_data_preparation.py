#!/usr/bin/env python

# Simone Fisicaro (2641824)

# import libraries
import pandas as pd
from time import strptime


# read data from the source folder
cons_m_input = pd.read_csv("../data/monthly_quarterly_electricity_consumption_monthly.txt", delimiter="\t", decimal=',')
cons_q_input = pd.read_csv("../data/monthly_quarterly_electricity_consumption_quarterly.txt", delimiter="\t", decimal=',')

# remove unwanted columns
cons_m_dropped = cons_m_input.drop(columns=["pds_energy_available", "pds_setc_industrial", "pds_setc_domestic", "pds_setc_other", "og_electricity_available", "og_losses_and_statistical_differences", "og_consumption_of_electricity", "aes_electricity_available", "aes_losses_and_statistical_differences", "aes_consumption_of_electricity"])
cons_q_dropped = cons_q_input.drop(columns=["pds_energy_available", "pds_setc_industrial", "pds_setc_domestic", "pds_setc_other", "og_electricity_available", "og_losses_and_statistical_differences", "og_consumption_of_electricity", "aes_electricity_available", "aes_losses_and_statistical_differences", "aes_consumption_of_electricity"])

# create quarter column and convert month column to number
cons_m_converted = cons_m_dropped
cons_q_converted = cons_q_dropped

cons_m_converted['month'] = cons_m_converted['month'].map(lambda x: strptime(x.replace('*', '').strip(), '%B').tm_mon)

cons_q_converted = cons_q_converted.rename(index=str, columns={"month": "quarter"})
cons_q_converted['quarter'] = cons_q_converted['quarter'].map(lambda x: x.replace('Quarter', '').strip())

# filter obs >= 2010
cons_m_filtered = cons_m_converted[cons_m_converted.year >= 2010]
cons_q_filtered = cons_q_converted[cons_q_converted.year >= 2010]

# save dataframes
cons_m_filtered.to_csv("../data/consumption_monthly.csv", index=False)
cons_q_filtered.to_csv("../data/consumption_quarterly.csv", index=False)

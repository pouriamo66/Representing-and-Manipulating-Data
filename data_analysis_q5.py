#!/usr/bin/env python

# Simone Fisicaro (2641824)

# import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# read data from the source folder
prod_input = pd.read_csv("../data/generation.csv")
cons_m_input = pd.read_csv("../data/consumption_monthly.csv")
cons_q_input = pd.read_csv("../data/consumption_quarterly.csv")


# filter obs >= 2013
cons_m_filtered = cons_m_input[cons_m_input.year >= 2013]
cons_q_filtered = cons_q_input[cons_q_input.year >= 2013]
prod_filtered = prod_input[prod_input.year >= 2013]


# correlation between month and demand
ax = sns.swarmplot(x="month", y="pds_setc_total", data=cons_m_input, palette="muted")
ax.set(xlabel='Month', ylabel='Electricity in TWh')
plt.show()


# country analysys through the year
sns.set()
cons_m_input_grouped = cons_m_input[['month', 'pds_setc_england_and_wales', 'pds_setc_scotland', 'pds_setc_northern_ireland']].groupby('month').agg('mean')

cons_m_input_grouped.plot(figsize=(20,10), linewidth=5, fontsize=20)
plt.xlabel('Month', fontsize = 20)
plt.ylabel('Electricity in TWh', fontsize = 20)


# consumption trend
ax = sns.relplot(x="month", y="pds_setc_total", hue="year", kind="line", data=cons_m_input, legend="full")
ax.set(xlabel='Month', ylabel='Electricity in TWh')
plt.ylim(20, 34)
plt.xlim(1, None)
plt.xticks(range(1, 13))


# analyse the quarterly production
sns.set()
prod_input_grouped = prod_input[['quarter', 'generated_hydro', 'generated_wind_solar_onshore', 'generated_of_which_offshore', 'generated_bioenergy']].groupby('quarter').agg('mean')
prod_input_grouped.plot(kind='bar')

plt.xlabel('Quarter')
plt.ylabel('Electricity in TWh')
plt.legend(['Hydro', 'Wind and Solar On-shore', 'Wind and Solar Off-shore', 'Bioenergy'], loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.show()

ax = sns.relplot(x="quarter", y="generated_renewable", hue="year", kind="line", data=prod_input, legend="full")
ax.set(xlabel='Month', ylabel='Electricity in TWh')
plt.ylim(0, 35)
plt.xlim(1, None)
plt.xticks(range(1, 5))


# compare production - demand data
cons_2017 = cons_m_input[cons_m_input.year == 2017][['month', 'pds_setc_total']].rename(columns={"pds_setc_total": "consumption"})
cons_2017['quarter'] = pd.to_numeric(np.ceil(cons_2017['month'] / 3), downcast='integer')

prod_2017 = prod_filtered[prod_filtered.year == 2017][['quarter', 'generated_renewable']].rename(columns={"generated_renewable": "production"})
prod_2017['production'] = prod_2017['production'] / 3

tot_2017 = cons_2017.set_index('quarter').join(prod_2017.set_index('quarter'))
tot_2017['quarter'] = tot_2017.index
tot_2017_melt = pd.melt(tot_2017, id_vars=["quarter", "month"], var_name="type", value_name="value")


ax = sns.relplot(x="month", y="value", hue="type", style="quarter", kind="line", dashes=False, markers=True, data=tot_2017_melt, palette="muted")
ax.set(xlabel='Month', ylabel='Electricity in TWh')
plt.ylim(0, 35)
plt.xlim(0.5, None)
plt.xticks(range(1, 13))


# calculate % of consumption from renewable
tot_2017['percentage'] = (tot_2017['production'] / tot_2017['consumption']) * 100
tot_2017


# analyse the losses trend
ax = sns.relplot(x="month", y="pds_transmission_distribution_and_other_losses1", hue="year", kind="line", data=cons_m_input, legend="full")
ax.set(xlabel='Month', ylabel='Electricity in TWh')
plt.ylim(0, 5)
plt.xlim(1, None)
plt.xticks(range(1, 13))

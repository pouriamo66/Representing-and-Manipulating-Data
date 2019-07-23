
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

#importing csv file of renewable energy generators in the United Kingdom
ukdt = pd.read_csv(r'C:\Users\user\Desktop\python dataset\renewable_generators.csv')

#selecting columns for computation of total energy generated in 2018 and their technology used
ukenergy = ukdt.loc[ :, ['country', 'technology', 'latest_data', 'latest_mwh_p_a']]

#filtering data for 2018 only
uk2018 = ukenergy[ukenergy['latest_data'].str.contains("2018")]

#finding renewable energy produced in UK so far in 2018
total = uk2018.loc[ :, [ 'technology', 'latest_mwh_p_a']]
totalenergy = total.groupby(['technology']).sum()
print (totalenergy)


# In[2]:


#finding renewable energy produced by each UK country so far in 2018
countrygroup = uk2018.loc[ :, ['country', 'technology', 'latest_mwh_p_a']]
country = countrygroup.groupby(['country', 'technology']).sum()
print (country)



# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#importing xls file of electricity generated in the United Kingdom
ukdt = pd.read_excel(r'C:\Users\user\Desktop\python dataset\Fuel_used_in_electricity_generation_and_electricity_supplied.xls',
                     sheet_name='Annual')

#selecting the rows and colums containing type and amount of electricity generated
ukgenerated = ukdt.iloc[[68,69,70,71,72,73,74,75,76,77,78], [0,13,14,15,16,17,18,19,20]]

#writing column names
ukgenerated.columns = ['energy source','2010','2011','2012','2013','2014','2015', '2016', '2017']

#setting energy source as index
ukgenerated.set_index('energy source', inplace=True)
print (ukgenerated)


# In[3]:


# selecting from energy source only renewable energy sources 
ukrenewable = ukgenerated.iloc[4:9,:]
print (ukrenewable)


# In[ ]:





# In[6]:


#removing offshore generated energy since it is covered already in wind and solar
new=ukrenewable.drop(['- of which, Offshore'])


# In[7]:


new


# In[8]:


#summing up of energy coming from renewable sources to get the total sum
new= new.append(new.agg(['sum']))


# In[10]:


#total sum of renewable energy sources from 2010-2017 full year
new


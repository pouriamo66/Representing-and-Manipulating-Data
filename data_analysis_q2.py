import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
filefullpath = r"G:\desktop\Fuel used in electricity generation and electricity supplied.xls"
data = pd.read_excel(filefullpath,sheet_name="Quarter",usecols="A,BQ:CF",header=3,index_col=0)
data1=data[67:78]

#create a method to convert to percent
f1 = lambda x :'%.2f%%'  %  (x*100)

#add columns name
data1.columns=('2014.3','2014.4','2015.1', '2015.2','2015.3', '2015.4','2016.1', '2016.2','2016.3', '2016.4','2017.1', '2017.2','2017.3', '2017.4','2018.1','2018.2')

data2=data1[4:9]

#drop the row named "of which, Offshore"
data2=data2.drop(['- of which, Offshore'])

# add 4 columns for each period summary
data2.insert(16,'T0(2014.3-2015.2)',0)
data2.insert(17,'T1(2015.3-2016.2)',0)
data2.insert(18,'T2(2016.3-2017.2)',0)
data2.insert(19,'T3(2017.3-2018.2)',0)
for a1 in range(0,4):
    data2.iloc[:,16]=data2.iloc[:,16]+data2.iloc[:,a1]
for a2 in range(4,8):
    data2.iloc[:,17]=data2.iloc[:,17]+data2.iloc[:,a2]
for a3 in range(8,12):
    data2.iloc[:,18]=data2.iloc[:,18]+data2.iloc[:,a3]
for a4 in range(12,16):
    data2.iloc[:,19]=data2.iloc[:,19]+data2.iloc[:,a4]

#Select the summary of each period and save in new table "data3"
data3=data2.iloc[:,16:20]


#create a new dataframe to save the growth rate
data4 = pd.DataFrame(index=data3.index, columns=data3.columns)

#fill the new dataframe "data4" with 0
data4 = data4.fillna(0)

#Create a for loop to calculate the growth rate. The formula is (Current year generation-last year generation)/last year generation
for x in range(1, 4):
        data4.iloc[:,x]=(data3.iloc[:,x]-data3.iloc[:,x-1])/data3.iloc[:,x-1]

#add new row named total 
data4.loc["total"]=0

#use for loop calculate the summary
for y in range(0,4):
        data4.iloc[4,:]=data4.iloc[4,:]+data4.iloc[y,:]


#Select the last three period 
data4=data4.iloc[:,1:4]

#transfer the data4 by rows and columns and save in "data5"
data5=data4.transpose()

#plot the "data5"
t=data5.plot()
t.set_xticks([0,1,2])
t.set_xticklabels(data5.index)
t.set_yticks([-0.1,0,0.1,0.2,0.3,0.4])
labels11=['-10%','0%','10%','20%','30%','40%']
t.set_yticklabels(labels11)
plt.xlabel('Period')
plt.ylabel('percentage of the growth rate')



#show the plot
plt.show()

#transfer the data to percentage
for b1 in range(0,3):
    for b2 in range(0,5):
        data5.iloc[b1,b2]=f1(data5.iloc[b1,b2])




#save the table to csv file
data5.to_csv('G:\desktop\growthrate.csv')



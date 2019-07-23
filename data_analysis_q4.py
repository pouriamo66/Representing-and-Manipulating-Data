import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima_model import ARMA


#Extracting  Annual sheet from booklet and  Extracting the data which need to be used
def fetch_data():
    data = pd.read_excel("data/data.xlsx","Annual",index_col=0, header=2)
    del data['Unnamed: 1']
    data.columns.names = ['YEAR']
    data.index.names = ['Renewable Sources']
    data = data.dropna()
    data = data.iloc[52:62, :]
    return data

#converting data to array and reshape them.to make them ready  for regression model
def make_xy(data, field):
    yy = np.array(data.loc[field]).reshape(-1, 1)
    xx = np.array(data.columns).reshape(-1, 1)
    return xx, yy

#make a prediction by regression model
def predict_reg(x, y, years):
    model = LinearRegression(fit_intercept=True)
    model.fit(x, y)
    predict = model.predict(years)
    return predict

#fit regression model and make a prediction for years between 2018-2030 by using loop
yearsArray = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
mydata = fetch_data()
predict_percenrage = {}
for pyear in yearsArray:
    pred_dict = {'total': 0}
    for source in mydata.index:
        myx, myy = make_xy(mydata, source)
        pred_dict[source] = predict_reg(myx, myy, [[pyear]])[0, 0]
        pred_dict['total'] += pred_dict[source]
    pred_dict_percentage_year = {}
    for source in mydata.index:
        pred_dict_percentage_year[source] = pred_dict[source] / pred_dict['total']
    predict_percenrage[pyear] = pred_dict_percentage_year

# extrcting total prcentage  of renewable sources per year  between 2018 and 2030
re_sources = ['Hydro (natural flow) ', 'Wind and Solar', 'Bioenergy', 'Pumped Storage']

for pyear in yearsArray:
    total_percentage_green = 0
    for s in re_sources:
        total_percentage_green += predict_percenrage[pyear][s]
    print("total % green sorce for year {} is {}".format(pyear, total_percentage_green))


# in this part by using ARIMA method I tried to make prediction for 2020 and 2030 in confidens leve of 95%
data1=pd.read_excel("data/data.xlsx","Annual",index_col=0, header=2)
del data1['Unnamed: 1']
data1.columns.names = ['YEAR']
data1.index.names = ['Renewable Sources']
data1=data1.dropna()
newdata=data1.iloc[56:62,:]
total=data1.iloc[62,:]
newdata=newdata.drop(['Other fuels','- of which, Offshore'])
data2=(newdata/total)*100
data2.loc["Total%"]=0
for x in range(0,4):
 data2.iloc[4]=data2.iloc[4]+data2.iloc[x]

# preparing data for Arima test
df= data2.loc['Total%']
df1=pd.DataFrame(df)
df1.index = pd.to_datetime(df1.index,format='%Y')

# Forecast interest rates using an AR(1) model
mod = ARMA(df1, order=(2,0))
res = mod.fit()

# Plot the original series and the forecasted series
res.plot_predict(start=4, end='2030')
plt.legend(loc='upper left',fontsize=8)
plt.xlabel('Year')
plt.show()
#arima resulat summary
print(res.summary())
# -*- coding: utf-8 -*-
"""task one i 2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a4vqfjbilbX-whzBr-j2QZYfTIYSb2qQ
"""

# Import libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error


import os
for dirname, _, filenames in os.walk('/content/house-prices-advanced-regression-techniques.zip'):
  for filename in filenames:
    print(os.path.join(dirname,filename))



"""feature engneering

"""

df = pd.read_csv('/content/train.csv')

df

df.drop(['Id','Alley', 'MasVnrType', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature'], axis=1, inplace=True)
df.info()

df[['LotFrontage', 'MasVnrArea','Electrical']]
df['LotFrontage'] = df['LotFrontage'].replace(np.nan,df['LotFrontage'].mean())

df['MasVnrArea'] = df['MasVnrArea'].replace(np.nan,df['MasVnrArea'].mean())

df['Electrical'] = df['Electrical'].fillna(df['Electrical'].mode().iloc[0])

df['BsmtQual'] = df['BsmtQual'].replace(np.nan, 'unavailable')
df['BsmtCond'] = df['BsmtCond'].replace(np.nan, 'unavailable')
df['BsmtExposure'] = df['BsmtExposure'].replace(np.nan, 'unavailable')
df['BsmtFinType1'] = df['BsmtFinType1'].replace(np.nan, 'unavailable')
df['BsmtFinType2'] = df['BsmtFinType2'].replace(np.nan, 'unavailable')

df['GarageType'] = df['GarageType'].replace(np.nan, 'unavailable')
df['GarageYrBlt'] = df['GarageYrBlt'].replace(np.nan, 0)
df['GarageFinish'] = df['GarageFinish'].replace(np.nan, 'unavailable')
df['GarageQual'] = df['GarageQual'].replace(np.nan, 'unavailable')
df['GarageCond'] = df['GarageCond'].replace(np.nan, 'unavailable')

df['GarageCond']

df.info()

sns.heatmap(df.select_dtypes(exclude = 'object').corr())

df.select_dtypes(exclude = 'object').corr().loc['SalePrice']

for key, value in df.select_dtypes(exclude='object').corr().loc['SalePrice'].to_dict().items():
    if (value <0.5 ):
        df.drop([key], axis=1, inplace=True)
        print('Dropped ' + key)

df.plot(kind = 'box', subplots = True, layout = (2,7), sharex = False, sharey = False, figsize = (20, 10), color = 'k')
plt.show()

def outliers(data, drop=False):
    #Looping through numerical columns
    for feature in  data.select_dtypes(exclude='object').columns:
        if feature == 'SalePrice':
            continue
    #get the feature
        data_feature = data[feature]
    #get the Q1 and Q3
        Q1 = np.percentile(data_feature, 25.)
        Q3 = np.percentile(data_feature, 75.)
        iqr = Q3 - Q1
        outlier = iqr * 1.5
        filtered_data = data_feature[(data_feature < Q1 - outlier) | (data_feature > Q3 + outlier)].index.tolist()
        if not drop:
            print(f'{len(filtered_data)} outliers in {feature}')
        else:
            data.drop(filtered_data, inplace=True)
            print(f'outliers from {feature} removed')
outliers(df)

outliers(df, drop=True)
#Check outliers
df.plot(kind = 'box', subplots = True, layout = (2,7), sharex = False, sharey = False, figsize = (20, 10), color = 'k')
plt.show()

le = LabelEncoder()
for feature in df.select_dtypes(include='object').columns:
    if feature == 'GarageYrBlt':
        continue
    print('encoding ' + feature)
    df[feature] = le.fit_transform(df[feature])

X = df.drop('SalePrice', axis=1)
y = df['SalePrice']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

"""MOdeling

"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
 X_scaled, y, test_size=0.1, random_state=0)

X_train.shape, y_train.shape, X_test.shape, y_test.shape

import lightgbm as lgb
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
rf = RandomForestRegressor()

# Fit RandomizedSearchCV
rf.fit(X_train, y_train)
y_predict = rf.predict(X_test)
mse = mean_squared_error(y_test, y_predict)
mse
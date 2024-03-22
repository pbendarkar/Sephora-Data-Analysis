# -*- coding: utf-8 -*-
"""Sephora DataSet EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DoE3rzHY9rqFCU_yfFP_ffAf9nVFCm7f
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import plotly.express as px

#settings :
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 400)
pd.set_option('display.width', 150)
pd.set_option('display.max_colwidth',50)

data = pd.read_csv('/content/sephora_website_dataset.csv')


data.sample(5)

data.info()

data.describe()

data.name.value_counts(dropna=False)

data.corr() # Correlation between each columns

# Visualizing the correlation

plt.figure(figsize=(10,8))
sns.heatmap(data.corr(),annot=True)

# Different Type of products available on Sephora
pd.set_option('display.max_rows', None)
data.category.value_counts(dropna=False)

# What are the brands that is available at Sephora?

data.brand.value_counts()

# Visualizing brands that is available at Sephora

available_brands=data.brand.value_counts()
print("availabe brand at Sephora and amount")
px.bar(data_frame=available_brands)

# What are top 10 most favourite products by customers?

df=pd.DataFrame(data.groupby('category')['love'].mean()).reset_index().sort_values(by='love', ascending=False).reset_index().drop('index',axis=1)
df.head(10)

sliced_df=df.iloc[0:10]
print("Top 10 most loved Categories or products  at Sephora")
px.pie(sliced_df,names=sliced_df.category,values=sliced_df.love)

# what are the most expensive brands at Sephora ?¶
most_exp=pd.DataFrame(data.groupby('brand')['price'].max()).reset_index().sort_values(by='price', ascending=False).reset_index().drop('index',axis=1)
most_exp.head(20)

# Visualizing Top 20 most expensive brands at Sephora
px.bar(y='price', x='brand', data_frame=most_exp[:20])

#Most popular SkinCare Brand based on rating¶
data.loc[data.category == 'Skincare', :].sort_values('rating').head(5)

#What are the most frequent brands that got highest rating?¶
top_rank_brands = data.loc[data.rating== 5]
top_rank_brands.groupby(['brand','rating']).agg(lambda x: x.value_counts().index[0])[:5]

# What are the 5 most frequent brands that got lowest rating?¶
lowest_rank_brands = data.loc[data.rating== 1.0]
lowest_rank_brands.groupby(['brand','rating']).agg(lambda x: x.value_counts().index[0])[:5]

# What are the top 10 most exclusive products?¶
exclusive = data.groupby(['category'])['exclusive'].count().sort_values(ascending=False).reset_index()
exclusive.head(10)

#What are the top 10 most online only products?
online_only= data.groupby(['category'])['online_only'].count().sort_values(ascending=False).reset_index()
online_only.head(10)

#What are the top 10 brand that received the most frequent reviews from customers?¶

reviews = pd.DataFrame(data.groupby('brand')['number_of_reviews'].mean())
most_reviews = reviews.sort_values('number_of_reviews', ascending=False)
most_reviews.head(10)

#The most limited Edition brands¶
limited_edition= data.groupby(['brand'])['limited_edition'].count().sort_values(ascending=False).reset_index()
limited_edition.head(10)

sephora_collection=data.loc[data.brand=="SEPHORA COLLECTION"]
sephora_collection.groupby(['category','name']).sum()

#What is the Brand With the Most Sales?¶
plt.figure(figsize=(30,100),dpi=100)
plt.xticks(rotation=90)
plt.title('Brand Counts')
sns.countplot(y=data['brand'], palette="nipy_spectral");

brandbig10 = data.groupby(['brand'])['exclusive'].count().sort_values(ascending=False).reset_index().head(10)

plt.figure(figsize=(18,6), dpi=100)
plt.subplot(2,2,1)
plt.ylabel('')
plt.xlabel('')
sns.barplot(y=brandbig10['brand'],x=brandbig10['exclusive'], palette='nipy_spectral')

features = ['number_of_reviews','love','price','value_price']
plt.figure(figsize=(15, 10))
for i in range(0, len(features)):
    plt.subplot(1, 4, i+1)
    sns.boxplot(y=data[features[i]],color='green',orient='v')
    plt.tight_layout()

data['number_of_reviews'] = np.log1p(data['number_of_reviews'])
data['love'] = np.log1p(data['love'])
data['price'] = np.log1p(data['price'])
data['value_price'] = np.log1p(data['value_price'])

plt.figure(figsize=(15, 7))
for i in range(0, len(features)):
    plt.subplot(1, 4, i+1)
    sns.boxplot(y=data[features[i]],color='green',orient='v')
    plt.tight_layout()

#Feature Engineering
data.info()

data = data.drop(['id'],axis=1)
data = data.drop(['name'],axis=1)
data = data.drop(['URL'],axis=1)
data = data.drop(['options'],axis=1)
data = data.drop(['details'],axis=1)
data = data.drop(['how_to_use'],axis=1)
data = data.drop(['ingredients'],axis=1)
data = data.drop(['price'],axis=1)

#Feature encoding (one hot encoding)
data['rating']=data['rating'].astype(str)

# Get all the categorical columns
cat_cols = data.select_dtypes("object").columns

## One-Hot Encoding all the categorical variables but dropping one of the features among them.
drop_categ = []
for i in cat_cols:
    drop_categ += [ i+'_'+str(data[i].unique()[-1]) ]

## Create dummy variables (One-Hot Encoding)
data = pd.get_dummies(data, columns=cat_cols)

## Drop the last column generated from each categorical feature
data.drop(drop_categ, axis=1, inplace=True)

#Modeling
from sklearn.linear_model import ElasticNet, Lasso,  BayesianRidge, LassoLarsIC
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score, train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn import metrics

from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

X = data.drop('value_price', axis = 1)
y = data['value_price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

#Standardization
# scaler = RobustScaler() #RobustScaler - StandardScaler
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)#

# lets print the shapes again
print("Shape of the X Train :", X_train.shape)
print("Shape of the y Train :", y_train.shape)
print("Shape of the X test :", X_test.shape)
print("Shape of the y test :", y_test.shape)

# Model Build
from sklearn.metrics import confusion_matrix, classification_report,accuracy_score,roc_curve, auc, precision_recall_curve, f1_score
import warnings
warnings.filterwarnings('ignore')

xgb = XGBRegressor()

xgb.fit(X_train, y_train)
data_imp = pd.DataFrame(xgb.feature_importances_ , columns = ['Importance'], index=X_train.columns)
data_imp = data_imp.sort_values(['Importance'], ascending = False)

data_imp.head()

XGB_model = XGBRegressor()

XGB_model.fit(X_train, y_train)
y_pred= XGB_model.predict(X_test)

print("Accuracy on Traing set   : ",XGB_model.score(X_train,y_train))
print("Accuracy on Testing set  : ",XGB_model.score(X_test,y_test))
print("__________________________________________")
print("\t\tError Table")
print('Mean Absolute Error      : ', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared  Error      : ', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error  : ', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('R Squared Error          : ', metrics.r2_score(y_test, y_pred))

RandomForest = RandomForestRegressor()
RandomForest.fit(X_train, y_train)
y_pred= RandomForest.predict(X_test)

print("Accuracy on Traing set   : ",RandomForest.score(X_train,y_train))
print("Accuracy on Testing set  : ",RandomForest.score(X_test,y_test))
print("__________________________________________")
print("\t\tError Table")
print('Mean Absolute Error      : ', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error       : ', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error  : ', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('R Squared Error          : ', metrics.r2_score(y_test, y_pred))
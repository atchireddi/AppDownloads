__author__ = 'atchirc'

# import packages
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Read ranking data
rank = pd.read_csv('./input/ranking_info.csv')

# Extract hour infor from 'Hour' column.
rank['Ehour'] = [h.hour for h in pd.to_datetime(rank['Hour'])]

# Save ranking infor to output
rank.to_csv('./output/ranking_info.csv')

# SWITCH TO TABLEAU FOR ANALYSIS

df = rank.groupby(['App ID', 'Country', 'Date', 'Device'], as_index=False)['Rank'].agg({'MnRank' : [np.mean], 'MdRank' : [np.median], 'sd' : [np.std], 'HMnRank' : [stats.hmean]})
df.columns = df.columns.map(''.join)

df.to_csv('./output/daily_ranking.csv')


# SWITCH TO TABLEAU FOR ANALYSIS.


downloads = pd.read_csv('./input/download_info.csv')


# Merage rankings to downloads

df_mgr = pd.merge(downloads, df, on=['App ID','Country','Device','Date'],how='left')

# drop records missing mean info.
df_mgr = df_mgr.dropna()   

df_mgr.to_csv('./output/download_rank.csv')

# SWITCH TO TABLEAU FOR ANALYSIS.


# Prepare data for modeling.

# compile logRank
df_mgr['LnHMnRankhmean'] = np.log(df_mgr['HMnRankhmean'])

# compile days lapsed
daysLapsed = pd.to_datetime(df_mgr['Date']) - pd.to_datetime(min(df_mgr['Date']))
df_mgr['DaysLapsed'] = [d.days+1 for d in daysLapsed]


# Filter data for iPhone USA segment.
model_data = df_mgr.loc[df_mgr['Device'].isin(['iPhone']) & df_mgr['Country'].isin(['USA'])]


# Train and Test data split.
# As downloads show time(day) dependancy, will trip last 3days data for testing.
# will use Downloads as target(dependant) variable,
#  and HMnRankhmean(Harmonic Mean), DaysLapsed as indenpendent variable for linear regression.

train = model_data.loc[model_data['DaysLapsed']<12, ['DaysLapsed','LnHMnRankhmean','Downloads']] 
test  = model_data.loc[model_data['DaysLapsed']>11, ['DaysLapsed','LnHMnRankhmean','Downloads']] 


# Linear Model

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(train.iloc[:,:2], train.iloc[:,2])

# Make predictions using the testing set
downloads_pred = regr.predict(test.iloc[:,:2])


# Model Evaluation:  R2
print('Variance Score R2 : %.2f' % r2_score(test.iloc[:,2], downloads_pred))


# Plot outputs
fig = plt.figure()
plt.plot(test.iloc[:, 2], downloads_pred, 'b.')
fig.suptitle('Actual Vs Predicted', fontsize=20)
plt.xlabel('Actual', fontsize=18)
plt.ylabel('Predicted', fontsize=16)
fig.savefig('./output/ActualVsPredicted.jpg')
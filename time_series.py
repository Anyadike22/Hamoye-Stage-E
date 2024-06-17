# -*- coding: utf-8 -*-
"""Time_Series.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10wkLo0JbE6FNlCL6zSLgpApphXLJIjDz
"""

import pandas as pd
import numpy as np

import pandas as pd

# Load the dataset
file_path = 'household_power_consumption.txt'
data = pd.read_csv(file_path, sep=';', low_memory=False)

# Display basic information about the dataset
print(data.info())
print(data.head())

data.info()

data

# Combine Date and Time columns into a single datetime column

data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], dayfirst=True)

# Set DateTime as the index
data.set_index('DateTime', inplace=True)

# Drop the original Date and Time columns
data.drop(columns=['Date', 'Time'], inplace=True)

data

# Interpolate missing values
df_interpolated = data.interpolate(method='time')

# Display the DataFrame to verify changes
print(df_interpolated)

df_interpolated

df_interpolated.isnull().sum()

df_interpolated.info()

import pandas as pd
import numpy as np

# Assuming 'df_interpolated' is your Pandas DataFrame

# Replace '?' with NaN
df_interpolated = df_interpolated.replace('?', np.nan)

# List of columns to cast as float
columns_to_cast = ['Global_active_power', 'Global_reactive_power', 'Voltage',
                   'Global_intensity', 'Sub_metering_1', 'Sub_metering_2',
                   'Sub_metering_3']

# Casting each column as float after replacing '?' with NaN
for column in columns_to_cast:
    df_interpolated[column] = df_interpolated[column].astype(float)

# Now all specified columns are cast to float type and '?' are handled

df_interpolated.info()

df_interpolated.isnull().sum()

import pandas as pd

# Assuming 'df_interpolated' is your Pandas DataFrame with the '?' replaced by NaN

# Interpolating missing values using the default linear method
df_interpolated = df_interpolated.interpolate(method='linear', axis=0)

# Now 'df_interpolated' has the missing values filled by linear interpolation

df_interpolated.isnull().sum()

df_interpolated.info()

import pandas as pd

# Assuming 'df_interpolated' is your Pandas DataFrame with the '?' replaced by NaN

# Interpolating missing values using the default linear method
df_interpolated = df_interpolated.interpolate(method='linear', axis=0)

# Now 'df_interpolated' has the missing values filled by linear interpolation

df_interpolated.info()

df_interpolated.plot()

# Resample the dataset to one minute
resampled_data = df_interpolated.resample('1T').mean()

# Verify the resampled dataset
print(resampled_data.head())

!pip install statsmodels

!pip install tensorflow

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

#visualize the dataset

plt.figure(figsize=(10, 6))
plt.plot(df_interpolated)
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Time Series Data')
plt.show()

# Assuming you want to use the last 20% of the data as the test set
train_size = int(len(df_interpolated) * 0.8)
train_data = df_interpolated[:train_size]
test_data = df_interpolated[train_size:]

#One minute sampling and prophet model

#Resample the data to one minute using mean aggregation
data_resampled = df_interpolated.resample('1Min').mean()

# Reset the index
data_resampled = data_resampled.reset_index()

# Rename the columns for Prophet compatibility
data_resampled = data_resampled.rename(columns={'DateTime': 'ds', 'Global_active_power': 'y'})

!pip install prophet

from prophet import Prophet

# Create and fit the Prophet model
model = Prophet()
model.fit(data_resampled)

# Generate future timestamps for forecasting
future = model.make_future_dataframe(periods=1440, freq='Min')

# Make predictions
forecast = model.predict(future)

# Print the forecasted values
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Resample the dataset to daily
resampled_2 = df_interpolated.resample('1D').mean()

# Verify the resampled dataset
print(resampled_2.head())

resampled_2.head()

df_2 = resampled_2.sort_values('DateTime')

test_days = 300
train_data = resampled_2[:-test_days]
test_data = resampled_2[-test_days:]

model = Prophet()

# Renaming the columns to fit Prophet's requirements
train_data = train_data.rename(columns={'DateTime': 'ds', 'Global_active_power': 'y'})

# prompt: Using the daily sampling rate (sum), divide the data into a train and test set. The last 300 days is your test set and the first (x-300) days is your training set. Where x is the length of the dataset. Use Facebook Prophet to train a Univariate time series modeling using this time column (‘dt’ or ‘ds’) and the global_active_power (or ‘y’)

# Import necessary libraries
import pandas as pd
from prophet import Prophet

# Define the test and train set sizes
test_days = 300
train_data = resampled_2[:-test_days]
test_data = resampled_2[-test_days:]

# Rename the columns for Prophet compatibility
train_data = train_data.rename(columns={'DateTime': 'ds', 'Global_active_power': 'y'})

# Create and fit the Prophet model
model = Prophet()
model.fit(train_data)

# Make predictions on the test set
forecast = model.predict(test_data)

# Print the forecasted values
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Define the test and train set sizes
test_days = 300
train_data = resampled_2[:-test_days]
test_data = resampled_2[-test_days:]

# Rename the columns for Prophet compatibility
train_data = train_data.rename(columns={'DateTime': 'ds', 'Global_active_power': 'y'})

# Create and fit the Prophet model
model = Prophet()
model.fit(train_data)

#Creating future dates for prediction
future_dates = model.make_future_dataframe(periods=test_days, freq='D')

#Making predictions on the test set
predictions = model.predict(future_dates[-test_days:])

# Selecting the relevant columns from predictions
predictions = predictions[['ds', 'yhat']]

# Merging the predictions with the actual test data
test_results = pd.merge(test_data[['DateTime', 'Global_active_power']], predictions, left_on='DateTime', right_on='ds')

# Displaying the test results
print(test_results[['DateTime', 'Global_active_power', 'yhat']])

# prompt: build a time series model using the other variables these  variables  be added to the forecast model as a regressor on Facebook Prophet. So the six independent variables ['Global_reactive_power', 'Voltage','Global_intensity', 'Sub_metering_1','Sub_metering_2','Sub_metering_3'] will be [‘add1’, ‘add2’, ‘add3’, ‘add4’, ‘add5’, ‘add6’] as the regressors. Split the data into train and test as done



# Define the regressor names
regressor_names = ['Global_reactive_power', 'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']

# Create a copy of the train data
train_data_with_regressors = train_data.copy()

# Add the regressors to the train data
for i, regressor_name in enumerate(regressor_names):
    train_data_with_regressors[f'add{i+1}'] = train_data[regressor_name]

# Fit the Prophet model with the regressors
model = Prophet()
model.add_regressor('add1')
model.add_regressor('add2')
model.add_regressor('add3')
model.add_regressor('add4')
model.add_regressor('add5')
model.add_regressor('add6')
model.fit(train_data_with_regressors)

# Make predictions on the test data
future = model.make_future_dataframe(periods=test_days, freq='D')

# Add the regressors to the future data
for i, regressor_name in enumerate(regressor_names):
    future[f'add{i+1}'] = test_data[regressor_name]

forecast = model.predict(future)

# Print the forecasted values
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
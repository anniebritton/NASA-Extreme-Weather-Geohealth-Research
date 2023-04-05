# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is designed to process raw heat index data from a daily census tract-level* CSV and output the following files:

# Heat Index Event File: CSV containing daily binary data for heat index events by census tract*.
# Heat index events are defined as two or more days at <5th percentile and >95th percentile of the tract's mean HI. 
# "1" indicates days on which heat index events occur.

# Binary Heat Index File: CSV containing daily binary data by census tract representing days with and without a heat index over the "Caution" threshold (80 degrees F) based on https://www.weather.gov/ama/heatindex.
# "1" indicates days with a mean heat index over over the "Caution" threshold (80 degrees F)

# Detailed Heat Index File: CSV containing detailed daily string data by census tract based on levels defined here: https://www.weather.gov/ama/heatindex.
# Levels are: ['Safe', 'Caution', 'Extreme_Caution', 'Extreme_Danger']

# *Column headers in the CSVs indicate tract GEOIDs to differentiate multipart tracts, where a tract may be split and
# located in two different geographic areas. In this case, there is a unique GEOID for each part of the tract.
# See here for more info: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html


# import packages
import pandas as pd
import numpy as np

# Read in the raw mean heat index data from a CSV file
hi_df = pd.read_csv("/mnt/local_drive/britton/TX_temperature_events/mean_heat_index_raw_v2.csv")

# Convert the 'Date' column to a datetime format
hi_df['Date'] = pd.to_datetime(hi_df['Date'])

# Set the 'Date' column as the index for the dataframe
hi_df.set_index('Date', inplace=True)



###### Calculate binary HI events from raw mean HI ######

# function for heatwaves with the default percentile set at 95%
def heatwaves(df, perc=95):
    
    # create lead and lag dataframes    
    df_lead = df.shift(1)
    df_lag = df.shift(-1)

    # define function to apply the threshold and return binary values
    def apply_threshold(col):
        # calculate the threshold based on the specified percentile
        threshold = np.percentile(col, perc)
        # apply the threshold and return binary values
        return np.where((col >= threshold) & ((df_lag[col.name] >= threshold) | (df_lead[col.name] >= threshold)), 1, 0)
    # apply the threshold function to the input dataframe and create a new dataframe        
    heatwave_df = df.apply(apply_threshold)
    # return the new dataframe
    return heatwave_df

# run the function
heatwave_df = heatwaves(hi_df)

# check of column summations to see how many days of heat events over the study period
heatwave_df.sum()

# Export heat events
heatwave_df.to_csv('/mnt/local_drive/britton/TX_temperature_events/mean_heat_index_events_v2.csv')



###### Calculate binary risk days from raw mean HI ######
# 80 degree F threshold is based on https://www.weather.gov/ama/heatindex

# A function that will return a 1 if the HI was 80+ degrees F, and a ) otherwise
def binaryrisk(df, risktemp = 80):
    
    # Apply a lambda function that replaces values >= risktemp with 1 and values < risktemp with 0
    binary_df = df.apply(lambda col: np.where((col >= risktemp), 1, 0))
    # return the new dataframe
    return binary_df

# run the function across the mean HI data
binary_df = binaryrisk(hi_df)

# check the sums of days 80+ degrees F in the dataframe
binary_df.sum()

# Export heat events
binary_df.to_csv('/mnt/local_drive/britton/TX_temperature_events/mean_heat_index_binary_risk_days_v2.csv')



###### Calculate detailed risk days from raw mean HI ######
# Thresholds based on https://www.weather.gov/ama/heatindex

def detailed_risk(df):
    # Define the conditions for the risk categories using a list of boolean arrays
    conditions = [
        df < 80,
        (df >= 80) & (df < 90),
        (df >= 90) & (df < 103),
        (df >= 103) & (df < 124),
        df >= 124
    ]
    # Define the corresponding risk categories using a list of strings
    choices = ['Safe', 'Caution', 'Extreme_Caution', 'Danger', 'Extreme_Danger']
    # Use np.select to apply the conditions and choices to the input DataFrame, 
    # returning a new DataFrame with the risk categories assigned to each element
    return pd.DataFrame(np.select(conditions, choices), index=df.index, columns=df.columns)

# run the function across the mean HI data
detailed_df = detailed_risk(hi_df)

# check the tail of the data
detailed_df.tail()

# Export heat events
detailed_df.to_csv('/mnt/local_drive/britton/TX_temperature_events/mean_heat_index_detailed_risk_days_v2.csv')

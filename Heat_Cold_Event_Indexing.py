# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com
# Date Updated: 12/3/2022

# This script is designed to index mean temperature data from a daily census tract-level* CSV
# and output a CSV with 1s and 0s. Below, heat and cold events are defined as two or more days
# at <5th percentile and >95th percentile of the tract's mean temperature, respectively. 
# "1" indicates days on which cold/heat waves occur. The thresholds can be adjusted as necessary.

# *Column headers in the CSVs indicate tract GEOIDs to differentiate multipart tracts, where a tract may be split and
# located in two different geographic areas. In this case, there is a unique GEOID for each part of the tract.
# See here for more info: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html

# import packages
import pandas as pd
import numpy as np

######## Heat Event Indexing #########

# read in csv and set index
heat_df = pd.read_csv("/mnt/local_drive/britton/PRISM_data/PRISM_csvs/tmean_csvs/PRISM_daily_tmean_final.csv")
heat_df['Date'] = pd.to_datetime(heat_df['Date'])
heat_df.set_index('Date', inplace=True)

# calculate heat events
col_list = heat_df.columns
df_lead = heat_df.shift(1) # set up the leading column to compare to day ahead
df_lag = heat_df.shift(-1) # set up the lagging column to compare to day behind

for n in range(0, (len(col_list))):
    threshold = np.percentile(heat_df.iloc[:,n], 95) #setting the 95th percentile threshold
    heat_df.iloc[:,n] = np.where(
       ((heat_df.iloc[:,n] >= threshold) & ((df_lag.iloc[:,n] >= threshold) | (df_lead.iloc[:,n] >= threshold))), 1, 0
    )

heat_df.sum() # check of column summations to see how many days of heat events over the study period

# export heat events
heat_df.to_csv('/mnt/local_drive/britton/PRISM_data/PRISM_indexing/PRISM_tmean_heat_index.csv')


######## Cold Event Indexing #########

# read in csv and set index
cold_df = pd.read_csv("/mnt/local_drive/britton/PRISM_data/PRISM_csvs/tmean_csvs/PRISM_daily_tmean_final.csv")
cold_df['Date'] = pd.to_datetime(cold_df['Date'])
cold_df.set_index('Date', inplace=True)

# calculate cold events
col_list = cold_df.columns
df_lead = cold_df.shift(1) # set up the leading column to compare to day ahead
df_lag = cold_df.shift(-1) # set up the lagging column to compare to day 

for n in range(0, (len(col_list))):
    threshold = np.percentile(cold_df.iloc[:,n], 5) #setting the 5th percentile threshold
    cold_df.iloc[:,n] = np.where(
       ((cold_df.iloc[:,n] <= threshold) & ((df_lag.iloc[:,n] <= threshold) | (df_lead.iloc[:,n] <= threshold))), 1, 0
    )

cold_df.sum() # check of column summations to see how many days of heat events over the study period

# export cold events
cold_df.to_csv('/mnt/local_drive/britton/PRISM_data/PRISM_indexing/PRISM_tmean_cold_index.csv')

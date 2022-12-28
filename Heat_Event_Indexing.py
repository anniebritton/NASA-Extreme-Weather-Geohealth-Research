# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is designed to index mean temperature data from a daily census tract-level* CSV
# and output a CSV with 1s and 0s. Below, heat events are defined by default as two or more days
# at >95th percentile of the tract's mean temperature. "1" indicates days on which heat waves occur.
# The threshold can be adjusted as necessary.

# *Column headers in the CSVs indicate tract GEOIDs to differentiate multipart tracts, where a tract may be split and
# located in two different geographic areas. In this case, there is a unique GEOID for each part of the tract.
# See here for more info: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html

# import packages
import pandas as pd
import numpy as np

# read in csv and set index
heat_df = pd.read_csv("/mnt/local_drive/britton/PRISM_data/PRISM_csvs/tmean_csvs/PRISM_daily_tmean_final.csv")
heat_df['Date'] = pd.to_datetime(heat_df['Date'])
heat_df.set_index('Date', inplace=True)

# function for heatwaves with the default percentile set at 95%
def heatwaves(df, perc = 95):
    
    # set up the lead and lag columns
    col_list = df.columns
    df_lead = df.shift(1)
    df_lag = df.shift(-1)

    # loop through the columns based on the selected threshold, 
    # comparing each day to the day before and after
    for n in range(0, (len(col_list))):
        threshold = np.percentile(df.iloc[:,n], perc)
        df.iloc[:,n] = np.where(
           ((df.iloc[:,n] >= threshold) & ((df_lag.iloc[:,n] >= threshold) | (df_lead.iloc[:,n] >= threshold))), 1, 0
        )

# run the heatwaves function
heatwaves(heat_df)

heat_df.sum() # check of column summations to see how many days of heat events over the study period

# export heat events
heat_df.to_csv('/mnt/local_drive/britton/PRISM_data/PRISM_indexing/PRISM_tmean_heat_index.csv')
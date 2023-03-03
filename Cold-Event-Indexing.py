# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is designed to index mean temperature data from a daily census tract-level* CSV
# and output a CSV with 1s and 0s. Cold events are defined by default as two or more days
# at <5th percentile of the tract's mean temperature. "1" indicates days on which cold events occur. 
# The thresholds can be adjusted as necessary.

# *Column headers in the CSVs indicate tract GEOIDs to differentiate multipart tracts, where a tract may be split and
# located in two different geographic areas. In this case, there is a unique GEOID for each part of the tract.
# See here for more info: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html

# import packages
import pandas as pd
import numpy as np

# read in csv and set index
cold_df = pd.read_csv("/mnt/local_drive/britton/PRISM_data/PRISM_csvs/tmean_csvs/PRISM_daily_tmean_final.csv")
cold_df['Date'] = pd.to_datetime(cold_df['Date'])
cold_df.set_index('Date', inplace=True)

# function for cold snaps with the default percentile set at 5%
def coldwaves(df, perc=5):
    
    df_lead = df.shift(1)
    df_lag = df.shift(-1)

    def apply_threshold(col):
        threshold = np.percentile(col, perc)
        return np.where((col <= threshold) & ((df_lag[col.name] <= threshold) | (df_lead[col.name] <= threshold)), 1, 0)
        
    binary_df = df.apply(apply_threshold)
    
    return binary_df
        
# run the coldsnaps function
coldwave_df = coldwaves(cold_df)
    
coldwave_df.sum() # check of column summations to see how many days of heat events over the study period

# export cold events
coldwave_df.to_csv('/mnt/local_drive/britton/PRISM_data/PRISM_indexing/PRISM_tmean_cold_events.csv')

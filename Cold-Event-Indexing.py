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
def coldsnaps(df, perc = 5):
    
    # set up the lead and lag columns
    col_list = df.columns
    df_lead = df.shift(1)
    df_lag = df.shift(-1)

    # loop through the columns based on the selected threshold, 
    # comparing each day to the day before and after
    for n in range(0, (len(col_list))):
        threshold = np.percentile(df.iloc[:,n], perc)
        df.iloc[:,n] = np.where(
           ((df.iloc[:,n] <= threshold) & ((df_lag.iloc[:,n] <= threshold) | (df_lead.iloc[:,n] <= threshold))), 1, 0
    )
        
# run the coldsnaps function
coldsnaps(cold_df)
    
cold_df.sum() # check of column summations to see how many days of heat events over the study period

# export cold events
cold_df.to_csv('/mnt/local_drive/britton/PRISM_data/PRISM_indexing/PRISM_tmean_cold_index.csv')

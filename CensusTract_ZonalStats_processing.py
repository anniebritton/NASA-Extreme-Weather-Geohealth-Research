# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com
# Date Updated: 12/3/2022

# This script is built to take in a census tract shapefile and daily .tif data for a study period,
# produce an empty dataframe "map," and perform zonal statistics for each census tract GEOID area,
# inputting each daily, tract-level value into the empty data frame.

# It is a fairly slow script, so for processing I reccomend either running it in the background using
# Screen on the Linux terminal, or splitting it into different years and then joining yearly dataframes
# at the end of the process.

# Helpful Screen Commands
## attach - screen -r XXXXX, Xs is the ID of the Screen you would like to attach
## detach - ctrl+a d
## list - screen -list
## kill - ctrl+a k


# import packages

import geopandas as gpd
import rasterio
from rasterio.plot import show
import rasterstats
from rasterstats import zonal_stats
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

import warnings;
warnings.filterwarnings('ignore');

# read in the shapefile
tracts = gpd.read_file(r'/mnt/local_drive/britton/TX_census_tracts/tl_2019_48_tract.shp') 

# select tracts and convert into a pandas dataframe
tract_df = pd.DataFrame(tracts)

# convert pandas dataframe into a geopandas dataframe
tract_polygon = gpd.GeoDataFrame(tract_df, geometry = 'geometry', crs = tracts.crs)

# create a variable for the number of files in the directory
file_num = len(os.listdir(r'/mnt/local_drive/britton/PRISM_data/PRISM_daily_tmax')) + 1

# create a empty date dataframe
data_map = pd.DataFrame('', columns = ['Date'], index = np.arange(1, file_num))

# create a list for column headers that correspond to census tract GEOID's
tract_id_list = tract_df['GEOID'].to_list()

# create a tract_id dataframe and transpose to columns
tract_id_df = pd.DataFrame(tract_id_list).transpose()
tract_id_df.columns = tract_id_df.iloc[0] 
tract_id_df = tract_id_df[1:]

# concatenate the two dfs
frames = [data_map, tract_id_df]
data_map = pd.concat(frames, axis=1)

# change NaN values to an empty string
data_map = data_map.replace(np. nan,'',regex=True)

# write a for loop that runs through each raster in the folder, 
# takes the spatial average for each census tract,
# and appends the mean value to the data map created above

for n in range(1, (len(tract_id_list)+1)):
    
    i = 1
    
    print(round(n / len(tract_id_list) * 100, 2),"%", end="\r") # this prints a % of how far through the processing the script is based on the # of columns
  
    for rast in os.listdir(r'/mnt/local_drive/britton/PRISM_data/PRISM_daily_tmax'):
          if rast[-4: ] == '.tif':
            tmax = rasterio.open(r'/mnt/local_drive/britton/PRISM_data/PRISM_daily_tmax' + '//' + rast)
            tmax_array = tmax.read(1)
            affine = tmax.transform

            tract_average = zonal_stats(tract_polygon[(n-1):n],
                                                        tmax_array,
                                                        affine = affine, 
                                                        stats = ['mean'],
                                                        all_touched = True,
                                                        geojason_out = False)

            tract_average = tract_average[0]['mean']
            
            if n == 1:
                data_map.loc[i]['Date'] = rast[11:-4] # this adds a date column during the first iteration of the loop
            
            data_map.iloc[(i-1):i, n] = tract_average

            i = i + 1
    
data_frame = data_map            

# convert the dates to a readable date time format and sort by date
data_frame['Date'] = pd.to_datetime(data_frame['Date'], infer_datetime_format = True)
data_frame['Date'] = data_frame['Date'].dt.date
data_frame = data_frame.sort_values(by = 'Date')

# print to check the data_frame before export
data_frame

# export the dataframe to CSV
data_frame.to_csv('/mnt/local_drive/britton/PRISM_data/PRISM_daily_tmax.csv')

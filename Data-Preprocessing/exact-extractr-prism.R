# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is built to take in a census tract shapefile and daily .tif data for a study period
# and perform zonal statistics to find the mean for each census tract GEOID area.
# This script uses the exactextractr package to extract means using weighted averages
# based on the percentage of each pixel that the census tract covers.
# Using the exactextractr method is faster and more accurate than similar packages (rasterstats for Python).

library(exactextractr)
library(sf)
library(raster)
library(rgdal)
library(tidyverse)

# write a function to extract census level data using exact extract
extract_prism_data <- function(folder, shp, tiff_type, output_file) {
  setwd(paste0(folder, tiff_type))
  
  # Read the shapefile into an sf object
  shp_data <- st_read(shp)
  
  #create a list of files in the directory
  file_list <- list.files()
  
  # write a for loop to loop through each file
  for (file in file_list) {
    file_data <- raster(file)
    date <- str_sub(file, -14, -5) # extract the date for each file
    # Extract the mean daily values for each census tract
    shp_data[[date]] <- exact_extract(file_data, shp_data, 'mean')
  }
  
  # Turn the data into a df
  prism_data = as.data.frame(shp_data)
  
  # Reorder the columns
  prism_data = prism_data %>%
    select(GEOID, `2015-01-01`:last_col())
  
  # Create a list of GEOIDs
  geoids = prism_data$GEOID
  
  # Transpose the data
  prism_data = t(prism_data)
  
  # Change the column names to the geiods
  colnames(prism_data) = geoids
  
  # Save as a csv
  write.csv(prism_data, paste0("/mnt/redwood/local_drive/britton/PRISM_data/PRISM_csvs/", output_file))
}

# create variables for the shapefile and file folder paths
folder = "/mnt/redwood/local_drive/britton/PRISM_data/PRISM_tifs/"
shp = "/mnt/redwood/local_drive/britton/TX_census_tracts/tl_2019_48_tract.shp"

# Call the function twice with different input values
extract_prism_data(folder, shp, "PRISM_daily_tmax", "PRISM_daily_tmax_v2.csv")
extract_prism_data(folder, shp, "PRISM_daily_tmin", "PRISM_daily_tmin_v2.csv")
extract_prism_data(folder, shp, "PRISM_daily_tmean", "PRISM_daily_tmean_v2.csv")
extract_prism_data(folder, shp, "PRISM_daily_tdmn", "PRISM_daily_tdmn_v2.csv")
extract_prism_data(folder, shp, "PRISM_daily_ppt", "PRISM_daily_ppt_v2.csv")
extract_prism_data(folder, shp, "PRISM_daily_vpdmax", "PRISM_daily_vpdmax_v2.csv")
extract_prism_data(folder, shp, "PRISM_daily_vpdmin", "PRISM_daily_vpdmin_v2.csv")


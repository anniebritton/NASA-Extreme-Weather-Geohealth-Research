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
extract_grid_data <- function(folder, shp, tiff_type, output_file) {
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
  grid_data = as.data.frame(shp_data)
  
  # Reorder the columns
  grid_data = grid_data %>%
    select(GEOID, `2015-01-01`:last_col())
  
  # Create a list of GEOIDs
  geoids = grid_data$GEOID
  
  # Transpose the data
  grid_data = t(grid_data)
  
  # Change the column names to the geiods
  colnames(grid_data) = geoids
  
  # Save as a csv
  write.csv(grid_data, paste0('/mnt/redwood/local_drive/britton/gridMET_data/gridMET_csvs/', output_file))
}

# create variables for the shapefile and file folder paths
folder = "/mnt/redwood/local_drive/britton/gridMET_data/gridMET_tifs/"
shp = "/mnt/redwood/local_drive/britton/TX_census_tracts/tl_2019_48_tract.shp"

# Call the function twice with different input values
extract_grid_data(folder, shp, "gridMET_srad", "gridMET_daily_srad_v2.csv")
extract_grid_data(folder, shp, "gridMET_vs", "gridMET_daily_vs_v2.csv")
extract_grid_data(folder, shp, "gridMET_rmax", "gridMET_daily_rmax_v2.csv")
extract_grid_data(folder, shp, "gridMET_rmin", "gridMET_daily_rmin_v2.csv")


# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is built to take in a census tract shapefile and a NetCDF with daily data for a study period
# and perform zonal statistics to find the mean for each zipcode/census tract in a shapefile.
# This script uses the exactextractr package to extract means using weighted averages
# based on the percentage of each pixel that the census tract covers.
# Using the exactextractr method is faster and more accurate than similar packages (rasterstats for Python).


library(exactextractr)
library(sf)
library(raster)
library(rgdal)
library(ncdf4)
library(tidyverse)

# Function to extract data
extract_ncdf_data <- function(nc_path, shp_path, var_names, output_dir) {
  # Read the shapefile into an sf object
  shp_data <- st_read(shp_path)
  
  # Create a list of dates
  nc_time <- ncvar_get(nc_open(nc_path), "time") * 3600 # UPDATE TO MATCH DATETIME FORMAT OF YOUR DATA
  date_list <- as.character(as.POSIXct(nc_time, origin = "2016-11-04 19:00:00", tz = "UTC")) # UPDATE TO MATCH DATETIME FORMAT OF YOUR DATA
  
  # Loop through each variable
  for (var_name in var_names) {
    # Extract the data for each date
    data_map <- shp_data %>% as.data.frame() %>% select(ZCTA5CE20) # UPDATE TO MATCH GEOMETRY COLUMN NAME IN SHAPEFILE
    for (i in seq_along(date_list)) {
      file_data <- raster(nc_path, varname = var_name, band = i)
      file_flat <- calc(file_data, mean) 
      data_map[[date_list[i]]] <- exact_extract(file_flat, shp_data, 'mean') # Can also change "mean" here to whatever stat you need
    }
    
    # Transpose the data and save as a CSV
    data_t <- t(data_map[-1])
    colnames(data_t) <- data_map$ZCTA5CE20 # UPDATE TO MATCH GEOMETRY COLUMN NAME IN SHAPEFILE
    output_path <- file.path(output_dir, paste0(var_name, ".csv"))
    write.csv(data_t, output_path)
  }
}

# Call the function on your data
extract_ncdf_data(
  nc_path = "/mnt/redwood/local_drive/britton/VA_NLDAS_data/NLDAS_VA_combined_sorted_v2.nc4", # path to your NetCDF file
  shp_path = "/mnt/redwood/local_drive/britton/VA_zip_codes/tl_2020_us_zct_VA.shp", # path to your shapefile
  var_names = c("TMP", "SPFH", "PRES", "UGRD", "VGRD", "APCP", "DSWRF"), # variable names from the NetCDF that you would like to extract
  output_dir = "/mnt/redwood/local_drive/britton/VA_NLDAS_data/" # directory to output the csvs to
)

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

# create variables for the shapefile and file folder paths
shp = "/mnt/redwood/local_drive/britton/TX_census_tracts/tl_2019_48_tract.shp"
folder = "/mnt/redwood/local_drive/britton/FloodScan_data/FloodScan_tifs/"

# set working director to file folder
setwd(folder)

# Read the shapefile into an sf object
shp_data <- st_read(shp)

#create a list of files in the directory
file_list <- list.files(folder)

# write a for loop to loop through each file
for (file in file_list) {
  file_data <- raster(file)
  date <- str_sub(file, -14, -5) # extract the date for each file
  # Extract the mean daily values of SFED_AREA for each census tract
  shp_data[[date]] <- exact_extract(file_data, shp_data, 'mean')
}


# Turn the flood data into a df
flood_data = as.data.frame(shp_data)

# Reorder the columns
flood_data = flood_data %>%
  select(GEOID, `2015-01-01`:last_col())

# Create a list of GEOIDS
geoids = flood_data$GEOID

# Transpose the flood data
flood_data = t(flood_data)

# Change the column names to the geiods
colnames(flood_data) = geoids

# Save as a csv
write.csv(flood_data, "/mnt/redwood/local_drive/britton/FloodScan_data/floodscan_daily_sfed_v3.csv")

# Vizualize the V2 and V3 data to compare
v3 = read_csv("/mnt/redwood/local_drive/britton/FloodScan_data/FloodScan_daily_SFED_v3.csv")
v2 = read_csv("/mnt/redwood/local_drive/britton/FloodScan_data/FloodScan_daily_SFED_v2.csv")

v3_means = v3 %>% select(-Date) %>% colMeans()
v2_means = v2 %>% select(-Date) %>% colMeans()

plot(v3_means, v2_means, 
     xlab = "V3", 
     ylab = "V2",
     pch = 19, frame = FALSE,
     xaxt = "n", yaxt = "n")

# X-axis
axis(1, at = c(0, 0.01, 0.02, 0.03, 0.04))

# Y-axis
axis(2, at = c(0, 0.01, 0.02, 0.03, 0.04))

dev.off()

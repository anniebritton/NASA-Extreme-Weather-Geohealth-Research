# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is designed to calculate maximum, minimum, and mean heat index data 
# from daily census tract-level* CSVs of PRISM and gridMET data.

# *Column headers in the CSVs indicate tract GEOIDs to differentiate multipart tracts, where a tract may be split and
# located in two different geographic areas. In this case, there is a unique GEOID for each part of the tract.
# See here for more info: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html

library(tidyverse)
library(weathermetrics)

# import the premade variables
rmin <- read.csv("/mnt/redwood/local_drive/britton/gridMET_data/gridMET_csvs/V2_exactextract/gridMET_daily_rmin_v2.csv", row.names="Date", check.names=FALSE)
rmax <- read.csv("/mnt/redwood/local_drive/britton/gridMET_data/gridMET_csvs/V2_exactextract/gridMET_daily_rmax_v2.csv", row.names="Date", check.names=FALSE)
tmin <- read.csv("/mnt/redwood/local_drive/britton/PRISM_data/PRISM_csvs/V2_exactextract/PRISM_tmin_v2.csv", row.names="Date", check.names=FALSE)
tmax <- read.csv("/mnt/redwood/local_drive/britton/PRISM_data/PRISM_csvs/V2_exactextract/PRISM_tmax_v2.csv", row.names="Date", check.names=FALSE)
tmean <- read.csv("/mnt/redwood/local_drive/britton/PRISM_data/PRISM_csvs/V2_exactextract/PRISM_tmean_v2.csv", row.names="Date", check.names=FALSE)

# clean up rounding issues in the rmin and rmax data
rmin_clean <- as.data.frame(lapply(rmin, function(x) ifelse(x > 100, 100, ifelse(x < 0, 0, x))))
rmax_clean <- as.data.frame(lapply(rmax, function(x) ifelse(x > 100, 100, ifelse(x < 0, 0, x))))

# calculate rmean from the mins and maxes
rmean <- (rmin_clean + rmax_clean) / 2

# calculate the raw heat index data
heat_indexing <- function(t_df, rh_df) {
  final_hi <- lapply(seq_along(t_df), function(i) {
    t_vec <- t_df[[i]]
    rh_vec <- rh_df[[i]]
    
    heat_index <- heat.index(t = t_vec, 
                             rh = rh_vec,
                             temperature.metric = "fahrenheit", 
                             output.metric = "fahrenheit", 
                             round = 3)
    return(heat_index)
  })
  
  final_hi <- as.data.frame(final_hi)
  names(final_hi) <- names(t_df)
  rownames(final_hi) <- rownames(t_df)
  
  return(final_hi)
}

# run the function across the mean, max, and min data
mean_hi <- heat_indexing(tmean, rmean)
max_hi <- heat_indexing(tmax, rmax_clean)
min_hi <- heat_indexing(tmin, rmin_clean)

# export to csvs to keep raw data
write.csv(mean_hi, "/mnt/redwood/local_drive/britton/TX_temperature_events/mean_heat_index_raw_v2.csv")
write.csv(max_hi, "/mnt/redwood/local_drive/britton/TX_temperature_events/max_heat_index_raw_v2.csv")
write.csv(min_hi, "/mnt/redwood/local_drive/britton/TX_temperature_events/min_heat_index_raw_v2.csv")

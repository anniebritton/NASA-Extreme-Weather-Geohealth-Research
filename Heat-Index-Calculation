# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is designed to calculate maximum, minimum, and mean heat index data 
# from daily census tract-level* CSVs of PRISM and gridMET data.

# *Column headers in the CSVs indicate tract GEOIDs to differentiate multipart tracts, where a tract may be split and
# located in two different geographic areas. In this case, there is a unique GEOID for each part of the tract.
# See here for more info: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html

# load in libraries
library(tidyverse)
library(weathermetrics)

# import the census tract extracted variables derived from PRISM and gridMET data
rmin <- read.csv("/mnt/redwood/local_drive/britton/gridMET_data/gridMET_csvs/V2_exactextract/gridMET_daily_rmin_v2.csv", check.names=FALSE) # min relative humidity
rmax <- read.csv("/mnt/redwood/local_drive/britton/gridMET_data/gridMET_csvs/V2_exactextract/gridMET_daily_rmax_v2.csv", check.names=FALSE) # max relative humidity
tmin <- read.csv("/mnt/redwood/local_drive/britton/PRISM_data/PRISM_csvs/V2_exactextract/PRISM_tmin_v2.csv", check.names=FALSE) # min temperature
tmax <- read.csv("/mnt/redwood/local_drive/britton/PRISM_data/PRISM_csvs/V2_exactextract/PRISM_tmax_v2.csv", check.names=FALSE) # max temperature
tmean <- read.csv("/mnt/redwood/local_drive/britton/PRISM_data/PRISM_csvs/V2_exactextract/PRISM_tmean_v2.csv", check.names=FALSE) # mean temperature

# calculate rmean (mean relative humidity) from the mins and maxes
rmean <- (rmin[-1] + rmax[-1]) / 2
rmean$Date <- rmin[1]
rmean <- rmean %>% select(Date, everything())

# write a function calculate the raw heat index data
heat_indexing <- function(t_df, rh_df) {
  for (i in (length(t_df) - 1)) {
    t_vec <- t_df[[i+1]]
    rh_vec <- rh_df[[i+1]]
    
    final_hi <- t_df
    
    heat_index <- heat.index(t = t_vec, 
                            rh = rh_vec,
                            temperature.metric = "fahrenheit", 
                            output.metric = "fahrenheit", 
                            round = 3)
    final_hi[i+1] <- heat_index
  }
  return(final_hi)
}

# run the function across the mean, max, and min data
mean_hi <- heat_indexing(tmean, rmean)
max_hi <- heat_indexing(tmax, rmax)
min_hi <- heat_indexing(tmin, rmin)

# check the dfs
head(min_hi[1:4])
head(max_hi[1:4])
head(mean_hi[1:4])

# export to csvs to keep raw data
write.csv(mean_hi, "/mnt/redwood/local_drive/britton/TX_temperature_events/mean_heat_index.csv", row.names = FALSE)
write.csv(max_hi, "/mnt/redwood/local_drive/britton/TX_temperature_events/max_heat_index.csv", row.names = FALSE)
write.csv(min_hi, "/mnt/redwood/local_drive/britton/TX_temperature_events/min_heat_index.csv", row.names = FALSE)

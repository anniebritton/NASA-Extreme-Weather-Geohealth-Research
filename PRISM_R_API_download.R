# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com
# Date Updated: 12/3/2022

# This script is built to download PRISM daily maximum temperature (°C)
# data, clip it to the extent of Texas, and convert .bils to tifs. 
# Make sure to create and change the file paths before running the script!

################################################################################

# See documentation at the links below to change the "type" argument in the 
# get_prism_dailys() function to download other variables: 
# https://cran.r-project.org/web/packages/prism/vignettes/prism.html
# https://cran.r-project.org/web/packages/prism/prism.pdf
# For instance, changing the argument to type = "tmin" will provide minimum
# temperature data. I recommend changing the directory names as relevant below
# to reference the correct variable in place of "tmax".

############################# INSTALL AND IMPORT ###############################

install.packages('prism')
install.packages('raster')
install.packages('rgdal')
install.packages('stringr')
install.packages('sf')

library(prism) 
library(raster)
library(rgdal)
library(stringr)
library(sf)


################################# DOWNLOAD #####################################

# Set your download directory using `prism_set_dl_dir()`
# and create a variable for it to reference later on
prism_set_dl_dir("~/Documents/Research/Data/prism_daily_tmax") # MAKE SURE TO CHANGE FILE PATH!
org_dir = "~/Documents/Research/Data/prism_daily_tmax/" # MAKE SURE TO CHANGE FILE PATH!

# Download daily maximum temperature data
# You can change the date range and variable type as necessary below
get_prism_dailys(
  type = "tmax",
  minDate = "2016-01-01",
  maxDate = "2022-09-15",
  keepZip = FALSE
)

##################### EXTRACT FROM INDIVIDUAL FOLDERS ##########################

# Programmatically find each of the sub directories
my_files <- list.files(
  org_dir, 
  pattern = "PRISM", 
  recursive = TRUE, 
  include.dirs = FALSE)

# Your output directory to copy files to
new_dir <- "~/Documents/Research/Data/prism_daily_tmax_tifs" # MAKE SURE TO CHANGE FILE PATH!

# Make sure the directory exists (or create it!)
dir.create(new_dir, recursive = TRUE)

# Copy the files
for(file in my_files) {
  from = paste(org_dir, file, sep = "")
  file.copy(from = from, to = new_dir)
}

# Delete unneeded files
extensions = c('*.xml', '*.txt', '*.prj', '*.csv', '*.stx')
for (ext in extensions) {
  file.remove(list.files(path = new_dir, pattern = ext, full.names = TRUE))
}
  
################### FILE TYPE CONVERSION & CROP TO TX ##########################

# Define raster and shapefile variables
my_rasts <- list.files(new_dir, full.names = TRUE)
tx_boundary = st_read("~/Documents/Research/Data/Texas_State_Boundary/State.shp") # MAKE SURE TO CHANGE FILE PATH!

# Clip each raster to the extent of Texas and convert it to a .tif
for (rast in my_rasts) {
  if (str_sub(rast,-4,-1) == '.bil') {
    my_shape = tx_boundary 
    my_raster = raster(rast)
    output_name = (paste(str_sub(rast,1,-8), 'TX', '.tif', sep = ""))
    crop_rast = crop(my_raster, extent(my_shape))
    writeRaster(
      crop_rast, 
      output_name,
      format="GTiff",
      datatype='FLT4S',
      overwrite=FALSE)
  }
}

################################ CLEAN UP ######################################

# Remove final irrelevant files
extensions = c('*.hdr', '*.bil', '*.aux')
for (ext in extensions) {
  file.remove(list.files(path = new_dir, pattern = ext, full.names = TRUE))
}

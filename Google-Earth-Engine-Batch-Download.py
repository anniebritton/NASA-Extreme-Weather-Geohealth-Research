# Creator: Annie Britton, abritto4@jhu.edu, annie.eliz.britton@gmail.com

# This script is written to download data from Google Earth Engine using a batch method.
# Users must have a Google Earth Engine account set up.
# This example uses PRISM data (mean temperature) over the course of 2015.
# Data sources, assets, and dates are all interchangeable.

# installs and import libraries, if necessary
!pip install eefolium
!pip install pyshp # this is for importing the shapefile
!pip install geopandas # this is for importing the shapefile
!pip install geetools

import ee
import folium
import geetools
import pandas as pd
import geopandas
import json

# this will initialise ee, and you may need to copy and paste the authentication code
try:
        ee.Initialize()
except Exception as e:
        ee.Authenticate()
        ee.Initialize()


# import and create a variable for your shapefile
# in this case, we have uploaded a shapefile named "Texas" as an asset in GEE
texas = ee.FeatureCollection("projects/ee-annieelizbritton/assets/Texas")

# However, you can also import and create a variable for the shapefile like so:
# AOI_path = '/mnt/local_drive/britton/TX_census_tracts/tl_2019_48_tract.shp'
# texas = geemap.shp_to_ee(AOI_path)

# import PRISM data as an image collection
prism = ee.ImageCollection('OREGONSTATE/PRISM/AN81d').filterDate('2015-01-01','2016-01-01').filterBounds(texas).select('tmean')

# batch export to Google Drive
geetools.batch.Export.imagecollection.toDrive(
    prism, # select the image collection
    'PRISM_tmean', # change name of data/band as necessary
    namePattern='PRISM_tmean_{system_date}', # change name of data/band as necessary
    datePattern = 'y-MM-dd',
    scale=4000, # spatial resolution of the data
    region=texas, 
    extra=None, 
    verbose=False
)

# progress for the download can be found at https://code.earthengine.google.com/tasks

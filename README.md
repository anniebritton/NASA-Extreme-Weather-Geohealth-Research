# NASA-Extreme-Weather-Geohealth-Research
☂️🛰️ This work is for a NASA-funded project using Earth observations to improve methods available for estimating the health damages of extreme weather events in Texas.

Scripts are built to acquire, process, and analyze geospatial data relating to cold and heat events, flooding, and air quality across the state of Texas, but can be used for a variety of data products across different spatial extents.

This work is performed as part of Johns Hopkins University's [Hydroclimate Research Group](https://pages.jh.edu/bzaitch1/).

#### Data Inputs
 - <a href="https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2022&layergroup=Census+Tracts">US Census Tigerline Shapefile of Texas Census Tracts</a>
 - <a href="https://developers.google.com/earth-engine/datasets/catalog/OREGONSTATE_PRISM_AN81d">PRISM Daily Spatial Climate Dataset</a> (Variables: ppt, tdmean, tmax, tmin, tmean, vpdmax, vpdmin)
 - <a href="https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET">GRIDMET Gridded Surface Meteorological Dataset</a> (Variables: rmax, rmin, srad, vs)
 - <a href="https://www.aer.com/weather-risk-management/floodscan-near-real-time-and-historical-flood-mapping/">Floodscan SFED</a>

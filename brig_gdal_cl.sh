# GDAL and shell commands for preprocessing of BRIG data sets

# Bathymetry
# source data, GEBCO 2014
#  https://www.gebco.net/data_and_products/historical_data_sets/#gebco_2014
cd ‘/Users/arbailey/Google Drive/Shared drives/brigBH2021/data/source/gebco/GEBCO_2014’
gdal_translate -projwin -81.153002 27.946190 -71.277237 20.334728 GEBCO_2014_2D.nc gebco_2014_bahamas.tif
gdalwarp -overwrite -r bilinear -s_srs EPSG:4326 -t_srs EPSG:32618 -tr 900 900 gebco_2014_bahamas.tif /Users/arbailey/Google\ Drive/Shared\ drives/brigBH2021/data/work/bathytopo/gebco_2014_bahamas_32618.tif


# NASADEM
# Source:  NASADEM https://lpdaac.usgs.gov/products/nasadem_hgtv001/
# Downloaded 2021-08-11 from APPEARS, https://lpdaacsvc.cr.usgs.gov/appeears/task/area
# Elevation: NASADEM_NC.001_NASADEM_HGT_doy2000042_aid0001.tif
# Data Quality: NASADEM_NUMNC.001_NASADEM_NUM_doy2000042_aid0001.tif
# in /Users/arbailey/Google Drive/Shared drives/brigBH2021/data/source/nasadem

cd '/Users/arbailey/Google Drive/Shared drives/brigBH2021/data/source/nasadem'
# Subset and reproject into work directory
gdalwarp -overwrite -r bilinear -t_srs EPSG:32618 -tr 30 30 -tap -cutline ../../work/bhs_region.shp -crop_to_cutline NASADEM_NC.001_NASADEM_HGT_doy2000042_aid0001.tif ../../work/bathytopo/nasadem001_bahamas_32618.tif

# Also need the NASADEM_NUMNC layer to get the water mask pixels (value=0):
cd '/Users/arbailey/Google Drive/Shared drives/brigBH2021/data/source/nasadem'
gdalwarp -overwrite -r nearest -t_srs EPSG:32618 -tr 30 30 -tap -cutline ../../work/bhs_region.shp -crop_to_cutline NASADEM_NUMNC.001_NASADEM_NUM_doy2000042_aid0001.tif ../../work/bathytopo/nasadem001num_bahamas_32618.tif

Mask the HGT raster to include only land elevations.

gdal_calc.py -A NASADEM_NC.001_NASADEM_HGT_doy2000042_aid0001.tif -B NASADEM_NUMNC.001_NASADEM_NUM_doy2000042_aid0001.tif --co TILED=YES --co COMPRESS=LZW --overwrite --outfile NASADEM_HGT_landonly.tif --calc="(B>0)*A + (B==0)*(-32767)"

gdalwarp -overwrite -r bilinear -t_srs EPSG:32618 -tr 30 30 -tap -cutline ../../work/bhs_region.shp -crop_to_cutline NASADEM_HGT_landonly.tif ../../work/bathytopo/nasadem001land_bahamas_32618.tif

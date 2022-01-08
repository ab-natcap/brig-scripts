# fbd4gpop.sh
# GDAL commands for pre-processing Facebook data for Good Bahamas Population Data
#	Convert No Data pixels on land to zeros, and retain other no data pixels
#	Project to EPSG 32618 (UTM18N)

cd "/Users/arbailey/Google Drive/Shared drives/brigBH2021/data/work/pop"


### - General Population
# change no data pixels to zeros
# Source NoData = nan
gdal_calc.py -A ../../source/hdx/bhs_general_2020.tif --outfile=nanto0.tif --calc="nan_to_num(A,nan=0.0)" --NoDataValue=-99999 --overwrite 

# Mask raster to include only pixels on land (touched by shoreline poly).  All other will become No DAta
gdalwarp -overwrite \
  -cutline "/Users/arbailey/Google Drive/Shared drives/brigBH2021/data/work/shoreline/bhs_shore.gpkg" \
  -cl tnc_coastlinePlanet_2020 \
  -wo CUTLINE_ALL_TOUCHED=TRUE \
  nanto0.tif \
  intermediate.tif
# Then unset No Data so all water areas are value -99999
gdal_edit.py -unsetnodata -unsetstats intermediate.tif

# The shoreline does not touch all pixels with a population value, so paste them back in from the unmasked image
gdal_calc.py --overwrite -A intermediate.tif -B nanto0.tif --outfile fbd4g_bhs_general_2020_zeros.tif --calc="B*logical_and(A==-99999,B>0) + A*logical_and(A==-99999,B==0) + A*(A>=0)" --NoDataValue=-99999



### - Children under 5
# change no data pixels to zeros
# Source NoData = nan
gdal_calc.py -A ../../source/hdx/bhs_children_under_five_2020.tif --outfile=nanto0.tif --calc="nan_to_num(A,nan=0.0)" --NoDataValue=-99999 --overwrite

# Mask raster to include only pixels on land.  All other will become No DAta
gdalwarp -overwrite \
  -cutline "/Users/arbailey/Google Drive/Shared drives/brigBH2021/data/work/shoreline/bhs_shore.gpkg" \
  -cl tnc_coastlinePlanet_2020 \
  -wo CUTLINE_ALL_TOUCHED=TRUE \
  nanto0.tif \
  intermediate.tif
# Then unset No Data so all water areas are value -99999
gdal_edit.py -unsetnodata -unsetstats intermediate.tif

# The shoreline does not touch all pixels with a population value, so paste them back in from the unmasked image
gdal_calc.py --overwrite -A intermediate.tif -B nanto0.tif --outfile fbd4g_bhs_children_under_five_2020_zeros.tif --calc="B*logical_and(A==-99999,B>0) + A*logical_and(A==-99999,B==0) + A*(A>=0)" --NoDataValue=-99999



### - Elderly 60 plus
# change no data pixels to zeros
# Source NoData = nan
gdal_calc.py -A ../../source/hdx/bhs_elderly_60_plus_2020.tif --outfile=nanto0.tif --calc="nan_to_num(A,nan=0.0)" --NoDataValue=-99999 --overwrite

# Mask raster to include only pixels on land.  All other will become No DAta
gdalwarp -overwrite \
  -cutline "/Users/arbailey/Google Drive/Shared drives/brigBH2021/data/work/shoreline/bhs_shore.gpkg" \
  -cl tnc_coastlinePlanet_2020 \
  -wo CUTLINE_ALL_TOUCHED=TRUE \
  nanto0.tif \
  intermediate.tif
# Then unset No Data so all water areas are value -99999
gdal_edit.py -unsetnodata -unsetstats intermediate.tif

# The shoreline does not touch all pixels with a population value, so paste them back in from the unmasked image
gdal_calc.py --overwrite -A intermediate.tif -B nanto0.tif --outfile fbd4g_bhs_elderly_60_plus_2020_zeros.tif --calc="B*logical_and(A==-99999,B>0) + A*logical_and(A==-99999,B==0) + A*(A>=0)" --NoDataValue=-99999


## Delete intermediate files
rm nanto0.tif
rm intermediate.tif


## Reproject to EPSG:32618 (UTM18N, WGS-84)
gdalwarp -overwrite -r near -t_srs EPSG:32618 -co TILED=YES -co COMPRESS=LZW fbd4g_bhs_general_2020_zeros.tif fbd4g_bhs_general_2020_zeros_32618.tif
gdalwarp -overwrite -r near -t_srs EPSG:32618 -co TILED=YES -co COMPRESS=LZW fbd4g_bhs_children_under_five_2020_zeros.tif fbd4g_bhs_children_under_five_2020_zeros_32618.tif
gdalwarp -overwrite -r near -t_srs EPSG:32618 -co TILED=YES -co COMPRESS=LZW fbd4g_bhs_elderly_60_plus_2020_zeros.tif fbd4g_bhs_elderly_60_plus_2020_zeros_32618.tif


## Clip raster to include only area within 2km of shoreline as in 2017 analysis python notebook
gdalwarp -overwrite \
  -cutline ../shoreline/coastline_extract_2km_buffer.shp \
  -wo CUTLINE_ALL_TOUCHED=TRUE \
  -co TILED=YES -co COMPRESS=LZW \
  fbd4g_bhs_general_2020_zeros_32618.tif fbd4g_bhs_general_2020_zeros_2kmbuff_32618.tif

gdalwarp -overwrite \
  -cutline ../shoreline/coastline_extract_2km_buffer.shp \
  -wo CUTLINE_ALL_TOUCHED=TRUE \
  -co TILED=YES -co COMPRESS=LZW \
  fbd4g_bhs_children_under_five_2020_zeros_32618.tif fbd4g_bhs_children_under_five_2020_zeros_2kmbuff_32618.tif

gdalwarp -overwrite \
  -cutline ../shoreline/coastline_extract_2km_buffer.shp \
  -wo CUTLINE_ALL_TOUCHED=TRUE \
  -co TILED=YES -co COMPRESS=LZW \
  fbd4g_bhs_elderly_60_plus_2020_zeros_32618.tif fbd4g_bhs_elderly_60_plus_2020_zeros_2kmbuff_32618.tif
 
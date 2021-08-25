# tnc_benthic_vectorize.py
# Convert TNC benthic habitat from raster to vector & reproject the vector layer
# Third step of TNC Data processing - run after tnc_benthic_reclass.py

# https://www.e-education.psu.edu/geog489/node/2215
# https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#polygonize-a-raster-band

from osgeo import gdal, ogr, osr
import time
import datetime
import os
import pygeoprocessing as pygeo

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

def time_elapsed(start_time):
    """
    Calculate a string representation of  elapsed time given an input start time
    :param start_time: Start time
    :return: current time - start time formatted as hours:minutes:seconds
    """
    te = time.time() - start_time
    # print(str(datetime.timedelta(seconds=te)))
    return str(datetime.timedelta(seconds=te))

data_dir = '/Users/arbailey/natcap/brigbh2021/data/tnc/benthic'
drv = ogr.GetDriverByName('ESRI Shapefile')

def make_polys(in_raster, layername):
    # Input Raster source
    in_raster_path = os.path.join(data_dir, in_raster)
    raster = gdal.Open(in_raster_path)
    band = raster.GetRasterBand(1)
    prj = raster.GetProjection()
    print("Input: ", in_raster_path)
    print("NO DATA VALUE = ", band.GetNoDataValue())
    print("Projection is {}".format(prj))

    spatialRef = osr.SpatialReference()
    spatialRef.ImportFromWkt(prj)

    # Output shapefile
    out_shp = layername + '.shp'
    out_vector_path = os.path.join(data_dir, out_shp)
    outfile = drv.CreateDataSource(out_vector_path)
    print("Creating: ", out_vector_path)
    outlayer = outfile.CreateLayer(layername, srs=spatialRef )
    newField = ogr.FieldDefn('hab_code', ogr.OFTInteger)
    outlayer.CreateField(newField)

    # Raster --> polygon conversion
    gdal.Polygonize(band, band, outlayer, 0, [])

def proj_polys(layername):
    # Inpt shapefile
    in_shp = layername + '.shp'
    in_vector_path = os.path.join(data_dir, in_shp)
    print("Input: ", in_vector_path)
    # Output Shapefile
    out_epsg = 32618
    out_shp = ''.join((layername,'_',str(out_epsg),'.shp'))
    out_vector_path = os.path.join(data_dir, out_shp)
    print("Creating: ", out_vector_path)
    # Output spatial reference from EPSG code
    spatialRef = osr.SpatialReference()
    spatialRef.ImportFromEPSG(out_epsg)
    outWKT = spatialRef.ExportToWkt()
    # print(outWKT)
    pygeo.geoprocessing.reproject_vector(base_vector_path=in_vector_path,
                                         target_projection_wkt=outWKT,
                                         target_path=out_vector_path)

# Not Resampled
in_rasters = (
    'benhab_03042021_tnc_reef.tif',
    'benhab_03042021_tnc_coralalg.tif',
    'benhab_03042021_tnc_spurgrv.tif',
    'benhab_03042021_tnc_seagrass.tif'
)
out_layers = (
    'tnc_reef_poly',
    'tnc_coralalg_poly',
    'tnc_spurgrv_poly',
    'tnc_seagrass_poly'
)

# 12m Resampled
in_rasters = (
    'benhab_03042021_tnc_reef_12m.tif',
    'benhab_03042021_tnc_coralalg_12m.tif',
    'benhab_03042021_tnc_spurgrv_12m.tif',
    'benhab_03042021_tnc_seagrass_12m.tif'
)
out_layers = (
    'tnc_reef_poly_12m',
    'tnc_coralalg_poly_12m',
    'tnc_spurgrv_poly_12m',
    'tnc_seagrass_poly_12m'
)

# 20m Resampled
in_rasters = (
    'benhab_03042021_tnc_reef_20m.tif',
    'benhab_03042021_tnc_coralalg_20m.tif',
    'benhab_03042021_tnc_spurgrv_20m.tif',
    'benhab_03042021_tnc_seagrass_20m.tif'
)
out_layers = (
    'tnc_reef_poly_20m',
    'tnc_coralalg_poly_20m',
    'tnc_spurgrv_poly_20m',
    'tnc_seagrass_poly_20m'
)

# Masked Seagrass only
in_rasters = (
    'benhab_03042021_tnc_seagrass_masked1k.tif',
    'benhab_03042021_tnc_seagrass_12m_masked1k.tif',
    'benhab_03042021_tnc_seagrass_20m_masked1k.tif',
)
out_layers = (
    'tnc_seagrass_poly_masked1k',
    'tnc_seagrass_poly_12m_masked1k',
    'tnc_seagrass_poly_20m_masked1k',
)

for in_raster, out_layer in zip(in_rasters, out_layers):
    start_time = time.time()
    print("Vectorizing ", in_raster, " to", out_layer)
    make_polys(in_raster, out_layer)
    print("Projecting", out_layer, " to UTM 18N")
    proj_polys(out_layer)
    print("Processing time: {0}".format(time_elapsed(start_time)))

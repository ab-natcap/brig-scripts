# tnc_benthic_reclass.py
# Reclass TNC benthic raster into individual habitat type rasters
# Mask seagrass by distance from shore points (because it's too large to run in CV model otherwise)
# Second step of TNC Data processing - run after tnc_benthic_resample.py

# import os
# import numpy as np
# import xarray as xr
# import rioxarray as rxr

# data_dir = '/Users/arbailey/natcap/brigbh2021/data/tnc/benthic'

#### --- USING RIOXARRAY  --- Needs too much memory
#######  Process finished with exit code 137 (interrupted by signal 9: SIGKILL)
# OPen Source TNC benthic Raster
# in_raster = 'bh_benhab_03042021_merge_gridcode.tif'
# in_raster_path = os.path.join(data_dir, in_raster)
# benthic_all = rxr.open_rasterio(in_raster_path, chunks=True).squeeze()
# print("Processed: ", in_raster)
# print("CRS:  ", benthic_all.rio.crs)
# print("Spatial extent:  ", benthic_all.rio.bounds())
# print("Bands:  ", benthic_all.rio.count)
# print("Pixel size:  ", benthic_all.rio.resolution())
# print("No data value:  ", benthic_all.rio.nodata)
#
# # Reclassify Coral reef components into a single value, otherwise to no data value (15)
# reef = xr.where(benthic_all < 4, 1, 15)
# reef.rio.update_attrs({'_FillValue': 15.0}, inplace=True)
# # reef.rio.set_nodata(15,inplace=True)
# print("Reclassified Reef array")
# print("CRS:  ", reef.rio.crs)
# print("Spatial extent:  ", reef.rio.bounds())
# print("Bands:  ", reef.rio.count)
# print("Pixel size:  ", reef.rio.resolution())
# print("No data value:  ", reef.rio.nodata)
#
# out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_reef.tif')
# print("Exporting to", out_raster_path)
# reef.rio.to_raster(out_raster_path, dtype=np.uint8)
####  END USING RIOXARRAY  --- Needs too much memory


#### ---- USING pygeoprocessing

import os
from osgeo import gdal
import pygeoprocessing as pygeo
import time
import datetime

def time_elapsed(start_time):
    """
    Calculate a string representation of  elapsed time given an input start time
    :param start_time: Start time
    :return: current time - start time formatted as hours:minutes:seconds
    """
    te = time.time() - start_time
    # print(str(datetime.timedelta(seconds=te)))
    return str(datetime.timedelta(seconds=te))

def raster_reclass(source_path, reclassed_path, value_map):
    """

    :param source_path: input raster full path
    :param reclassed_path: output (reclassified)
    :param value_map: value map for the reclassification
    :return:
    """
    print("Reclassifying {0} to {1}", (source_path, reclassed_path))
    pygeo.geoprocessing.reclassify_raster(base_raster_path_band=(source_path, 1),
                                          target_raster_path=(reclassed_path),
                                          value_map=value_map,
                                          target_datatype=gdal.GDT_Byte,
                                          target_nodata=0,
                                          values_required=False,
                                          )

data_dir = '/Users/arbailey/natcap/brigbh2021/data/tnc/benthic'

# Source Rasters -- various resampled resolutions
in_raster_4m = 'bh_benhab_03042021_merge_gridcode.tif'
in_raster_12m = 'bh_benhab_03042021_merge_gridcode_12m.tif'
in_raster_20m = 'bh_benhab_03042021_merge_gridcode_20m.tif'
in_raster_paths = [os.path.join(data_dir, rast) for rast in (in_raster_4m,
                                                             in_raster_12m,
                                                             in_raster_20m)]

# Reef
start_time = time.time()
# value map
reef_vm = {
    1: 1,
    2: 1,
    3: 1,
}
out_reef_paths = [os.path.join(data_dir, rast) for rast in ('benhab_03042021_tnc_reef.tif',
                                                            'benhab_03042021_tnc_reef_12m.tif',
                                                            'benhab_03042021_tnc_reef_20m.tif')]
# print("Processing Reef classes")
# for in_rast_path, out_rast_path in zip(in_raster_paths, out_reef_paths):
#     print(in_rast_path, out_rast_path)
#     raster_reclass(in_rast_path, out_rast_path, reef_vm)
# print("Processing time: {0}".format(time_elapsed(start_time)))


# Coral/Algae
start_time = time.time()
# value map
coralalg_vm = {
    1: 0,
    2: 0,
    3: 0,
    4: 2,
}
out_coralalg_paths = [os.path.join(data_dir, rast) for rast in ('benhab_03042021_tnc_coralalg.tif',
                                                            'benhab_03042021_tnc_coralalg_12m.tif',
                                                            'benhab_03042021_tnc_coralalg_20m.tif')]
# print("Processing Coral/Algae class")
# for in_rast_path, out_rast_path in zip(in_raster_paths, out_coralalg_paths):
#     print(in_rast_path, out_rast_path)
#     raster_reclass(in_rast_path, out_rast_path, coralalg_vm)
# print("Processing time: {0}".format(time_elapsed(start_time)))


# Spur and Groove Coral
start_time = time.time()
# value map
spurgrv_vm = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 3,
}
out_spurgrv_paths = [os.path.join(data_dir, rast) for rast in ('benhab_03042021_tnc_spurgrv.tif',
                                                            'benhab_03042021_tnc_spurgrv_12m.tif',
                                                            'benhab_03042021_tnc_spurgrv_20m.tif')]
# print("Processing Spur and Groove Reef class")
# for in_rast_path, out_rast_path in zip(in_raster_paths, out_spurgrv_paths):
#     print(in_rast_path, out_rast_path)
#     raster_reclass(in_rast_path, out_rast_path, spurgrv_vm)
# print("Processing time: {0}".format(time_elapsed(start_time)))


# Seagrass
start_time = time.time()
# value map
seagrass_vm = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 4,
    13: 4,
}
out_seagrass_paths = [os.path.join(data_dir, rast) for rast in ('benhab_03042021_tnc_seagrass.tif',
                                                            'benhab_03042021_tnc_seagrass_12m.tif',
                                                            'benhab_03042021_tnc_seagrass_20m.tif')]
# print("Processing Seagrass classes")
# for in_rast_path, out_rast_path in zip(in_raster_paths, out_seagrass_paths):
#     print(in_rast_path, out_rast_path)
#     raster_reclass(in_rast_path, out_rast_path, seagrass_vm)
# print("Processing time: {0}".format(time_elapsed(start_time)))

#
# print("Masking Seagrass raster", out_raster_path)
#
# # Mask Seagrass Raster
# # Use the Shore Points from Bahamas CV run to create 1 km buffer for mask
# start_time = time.time()
#
# seagrass_raster_path = out_raster_path
# shoreline_buffer_path = os.path.join(data_dir,'shore_points_buffer_1km.shp')
# projected_buffer_path = os.path.join(data_dir,'shore_points_buffer_1km_lambert.shp')
# masked_seagrass_raster_path = os.path.join(data_dir,'benhab_03042021_tnc_seagrass_masked1k.tif')
# masked_seagrass_raster_path = os.path.join(data_dir,'benhab_03042021_tnc_seagrass_12m_masked1k.tif')
# masked_seagrass_raster_path = os.path.join(data_dir,'benhab_03042021_tnc_seagrass_20m_masked1k.tif')
#
# raster_wkt = pygeo.geoprocessing.get_raster_info(seagrass_raster_path)['projection_wkt']
# pygeo.geoprocessing.reproject_vector(
#     shoreline_buffer_path, raster_wkt, projected_buffer_path)
#
# pygeo.geoprocessing.mask_raster(
#     (seagrass_raster_path, 1),
#     projected_buffer_path,
#     masked_seagrass_raster_path)
#
# print("Processing time: {0}".format(time_elapsed(start_time)))

# Macroalgae
start_time = time.time()
# value map
algae_vm = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 6,
    7: 5,
}
out_algae_paths = [os.path.join(data_dir, rast) for rast in ('benhab_03042021_tnc_algae.tif',
                                                            'benhab_03042021_tnc_algae_12m.tif',
                                                            'benhab_03042021_tnc_algae_20m.tif')]
print("Processing Macroalgae classed")
for in_rast_path, out_rast_path in zip(in_raster_paths, out_algae_paths):
    print(in_rast_path, out_rast_path)
    raster_reclass(in_rast_path, out_rast_path, algae_vm)
print("Processing time: {0}".format(time_elapsed(start_time)))


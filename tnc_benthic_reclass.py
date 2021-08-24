import os
import numpy as np
import xarray as xr
import rioxarray as rxr

data_dir = '/Users/arbailey/natcap/brigbh2021/data/tnc/benthic'

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

in_raster = 'bh_benhab_03042021_merge_gridcode.tif'
in_raster = 'bh_benhab_03042021_merge_gridcode_12m.tif'
in_raster_path = os.path.join(data_dir, in_raster)

# Reef
start_time = time.time()
# value map
reef_vm = {
    1: 1,
    2: 1,
    3: 1,
}
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_reef.tif')
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_reef_12m.tif')

print("Processing Reef classes")
pygeo.geoprocessing.reclassify_raster(base_raster_path_band=(in_raster_path,1),
                                      target_raster_path=(out_raster_path),
                                      value_map=reef_vm,
                                      target_datatype=gdal.GDT_Byte,
                                      target_nodata=0,
                                      values_required=False,
                                      )
print("Processing time: {0}".format(time_elapsed(start_time)))

# Coral/Algae
start_time = time.time()
# value map
coralalg_vm = {
    1: 0,
    2: 0,
    3: 0,
    4: 2,
}
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_coralalg.tif')
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_coralalg_12m.tif')

print("Processing Coral/Algae class")
pygeo.geoprocessing.reclassify_raster(base_raster_path_band=(in_raster_path,1),
                                      target_raster_path=(out_raster_path),
                                      value_map=coralalg_vm,
                                      target_datatype=gdal.GDT_Byte,
                                      target_nodata=0,
                                      values_required=False,
                                      )
print("Processing time: {0}".format(time_elapsed(start_time)))

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
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_spurgrv.tif')
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_spurgrv_12m.tif')

print("Processing Spur and Groove Reef class")
pygeo.geoprocessing.reclassify_raster(base_raster_path_band=(in_raster_path,1),
                                      target_raster_path=(out_raster_path),
                                      value_map=spurgrv_vm,
                                      target_datatype=gdal.GDT_Byte,
                                      target_nodata=0,
                                      values_required=False,
                                      )
print("Processing time: {0}".format(time_elapsed(start_time)))

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
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_seagrass.tif')
out_raster_path = os.path.join(data_dir, 'benhab_03042021_tnc_seagrass_12m.tif')
print("Processing Seagrass classes")
pygeo.geoprocessing.reclassify_raster(base_raster_path_band=(in_raster_path,1),
                                      target_raster_path=(out_raster_path),
                                      value_map=seagrass_vm,
                                      target_datatype=gdal.GDT_Byte,
                                      target_nodata=0,
                                      values_required=False,
                                      )
print("Processing time: {0}".format(time_elapsed(start_time)))

# tnc_benthic_resample.py
# 2021-08-24
import os

# working locally to minimize Google Drive synchronizing delays (if any)
#  Then, copy results to GDrive
data_dir = '/Users/arbailey/natcap/brigbh2021/data/tnc/benthic'

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
in_raster_path = os.path.join(data_dir, in_raster)
in_rastername, ext = os.path.splitext(in_raster)
print(in_rastername)

grid_sizes = [12,20]
for out_gridsize in [12,20]:
    start_time = time.time()
    out_raster = in_rastername + "_" + str(out_gridsize) + "m" +".tif"
    out_raster_path = os.path.join(data_dir,out_raster)

    print("Resampling Raster to create: " + out_raster)
    pygeo.geoprocessing.warp_raster(base_raster_path=in_raster_path,
                                    target_pixel_size=(out_gridsize,out_gridsize),
                                    target_raster_path=out_raster_path,
                                    resample_method='mode')
    print("Processing time: {0}".format(time_elapsed(start_time)))


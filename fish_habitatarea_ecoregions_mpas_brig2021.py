# fish_habitatarea_ecoregions_mpas_brig2021.py
# Script modified from 2017 Bahamas Fisheries work fish_habitatarea_ecoregions_mpas.py

# calc area of each habitat per 13 ecoregions
# link MPAs to ecoregions
## SE Bahamas MPA only includes habitats in Acklins ecoregion (even though the MPA spans ecoregions)
# calc area of each habitat in each MPA
# deduct MPA areas from total

import rasterstats as rs
import pandas as pd
import geopandas as gpd
import os
# from osgeo import ogr

## Habitat Areas

base_dir = '/Users/arbailey/Google Drive/Shared drives/brigBH2021/models/Fisheries/fisheries_inputs'
out_dir =  '/Users/arbailey/Google Drive/Shared drives/brigBH2021/models/Fisheries/fisheries_outputs/fisheries_outputs_202201/habitat_preprocessing'

### --- zonal stats for seagrass area calcs - within 1km of coast

ecoregion_shp_path = os.path.join(base_dir,'eco_shelves_1kmcoast.shp')
# mpas_region_shp_path = os.path.join(base_dir,'mpas_inshelf_1kmcoast_2022_expandednetwork.shp')
mpas_region_shp_path = os.path.join(base_dir,'mpas_inshelf_1kmcoast_2021.shp') # Original MPA network (2021 Fall)

sg_raster_path = os.path.join(base_dir,'seagrass.tif')
sg_resln = 20 # 0.02 # (20 m)

ecoregions = gpd.read_file(ecoregion_shp_path)
mpas_region = gpd.read_file(mpas_region_shp_path)

print("Calculating Stats for Seagrass by Ecoregions....")
# Seagrass by Ecoregions
stats = rs.zonal_stats(ecoregions, sg_raster_path,
               prefix='sea_', stats='count', geojson_out=True, alltouched=True)
eco_sea_stats = gpd.GeoDataFrame.from_features(stats)
eco_sea_stats.set_crs(ecoregions.crs, inplace=True)
print("Calculating Stats for Seagrass by MPAS....")
# Seagrass in MPAs
stats = rs.zonal_stats(mpas_region, sg_raster_path,
               prefix='sea_', stats='count', geojson_out=True, alltouched=True)
mpa_sea_stats = gpd.GeoDataFrame.from_features(stats)
mpa_sea_stats.set_crs(mpas_region.crs, inplace=True)

eco_sea_stats['sea_m2'] = eco_sea_stats.sea_count*(sg_resln * sg_resln) # cell dimensions in m
mpa_sea_stats['seampa_m2'] = mpa_sea_stats.sea_count*(sg_resln * sg_resln) # cell dimensions in m

# Check columns & projection info - for debugging
# print(eco_sea_stats.columns)
# print(eco_sea_stats.crs)
# print(mpa_sea_stats.columns)
# print(mpa_sea_stats.crs)

# Sum all seagrass area in MPAs by region
mpasea_area_byregion = mpa_sea_stats[['bankregion', 'seampa_m2']].groupby('bankregion').sum()
mpasea_area_byregion.reset_index(inplace=True)
# print(mpasea_area_byregion)



### ----- Zonal stats for mangrove area calcs - within 250m of coast

# converted shapefile to to raster prior to running this script:
# mangrove polygon data located here:  ../Mangroves.shp
# gdal_rasterize -burn 1 -a_nodata -9999 -tr 30.0 30.0 -l Mangrove Mangrove.shp Mangrove.tif

ecoregion_shp_path = os.path.join(base_dir,'eco_shelves_250mcoast.shp')
# mpas_region_shp_path = os.path.join(base_dir,'mpas_inshelf_250mcoast_2022_expandednetwork.shp')
mpas_region_shp_path = os.path.join(base_dir,'mpas_inshelf_250mcoast_2021.shp') # Orginal MPA network

mang_raster_path = os.path.join(base_dir,'Mangrove.tif')
mang_resln = 30 # 0.03 # (30 m)

ecoregions = gpd.read_file(ecoregion_shp_path)
mpas_region = gpd.read_file(mpas_region_shp_path)

print("Calculating Stats for Mangroves by Ecoregions....")
# Mangroves by Ecoregions
stats = rs.zonal_stats(ecoregions, mang_raster_path,
               prefix='mang_', stats='count', geojson_out=True, alltouched=True)
eco_mang_stats = gpd.GeoDataFrame.from_features(stats)

# Mangroves by MPAs
print("Calculating Stats for Mangroves by MPAS....")
stats = rs.zonal_stats(mpas_region, mang_raster_path,
               prefix='mang_', stats='count', geojson_out=True, alltouched=True)
mpa_mang_stats = gpd.GeoDataFrame.from_features(stats)

eco_mang_stats['mang_m2'] = eco_mang_stats.mang_count*(mang_resln * mang_resln) # cell dimensions in m
mpa_mang_stats['mangmpa_m2'] = mpa_mang_stats.mang_count*(mang_resln * mang_resln) # cell dimensions in m

# Check columns & projection info - for debugging
# print(eco_mang_stats.columns)
# print(eco_mang_stats.crs)
# print(mpa_mang_stats.columns)
# print(mpa_mang_stats.crs)

mpamang_area_byregion = mpa_mang_stats[['bankregion', 'mangmpa_m2']].groupby('bankregion').sum()
mpamang_area_byregion.reset_index(inplace=True)
# print(mpamang_area_byregion)

# Join MPA Habitat Summary stats   (Seagrass and Mangrove by MPA
mpa_hab_summary = mpa_mang_stats.merge(mpa_sea_stats[['mpa_name', 'bankregion', 'seampa_m2']], how='inner', on=['mpa_name', 'bankregion'])
mpa_hab_summary.sort_values(by=['mpa_name'], inplace=True)
# print(mpa_hab_summary)
# print(mpa_hab_summary.columns)


# OUtput MPA habitat Summary stats
mpahabsummary_file = 'mpa_habitat_summary_20220208_originalMPAnetwork.csv'
mpa_hab_summary_csvpath = os.path.join(out_dir,mpahabsummary_file)
print("Output file with habitat summary by MPA:", mpa_hab_summary_csvpath)
mpa_hab_summary[['mpa_name', 'bankregion', 'mangmpa_m2', 'seampa_m2']].to_csv(mpa_hab_summary_csvpath, index=False)


### Stats Joins
print("Joining stats together for ecoregions")
ecoregion_shp_path = os.path.join(base_dir,'ecoregions4lobster_32618.shp')
ecoregions = gpd.read_file(ecoregion_shp_path)
print(ecoregions)
print(ecoregions.columns)
eco1 = ecoregions.merge(eco_mang_stats[['bankregion', 'mang_m2']], on='bankregion')
eco2 = eco1.merge(eco_sea_stats[['bankregion', 'sea_m2']], on='bankregion')
eco3 = eco2.merge(mpasea_area_byregion, on='bankregion', how='left')
eco_m2 = eco3.merge(mpamang_area_byregion, on='bankregion', how='left')
print(eco_m2.columns)
print(eco_m2)
eco_m2.drop(axis=1, labels=['fid','ID', 'geometry'], inplace=True)
# # nan values generated because there are no MPAs in those regions. Replace with 0s
eco_m2.fillna(0.0, inplace=True)
eco_m2['mang_m2_scen'] = eco_m2.mang_m2 - eco_m2.mangmpa_m2
eco_m2['sea_m2_scen'] = eco_m2.sea_m2 - eco_m2.seampa_m2
eco_m2['sea_change'] = (eco_m2.sea_m2_scen - eco_m2.sea_m2)/eco_m2.sea_m2
eco_m2['mang_change'] = (eco_m2.mang_m2_scen - eco_m2.mang_m2)/eco_m2.mang_m2
eco_m2.fillna(0.0, inplace=True)
eco_m2.sort_values(by=['bankregion'], inplace=True)
eco_m2.rename(columns={'bankregion': 'ecoregion'})
print(eco_m2.head())
print(eco_m2.columns)

lobsterhabscenario_file = 'lobsterhabitat_scenariodata_20220208_originalMPAnetwork.csv'
lobster_hab_scenario_csvpath = os.path.join(out_dir, lobsterhabscenario_file)
print("Output file with lobster habitat scenario by ecoregion:", lobster_hab_scenario_csvpath)
eco_m2.to_csv(lobster_hab_scenario_csvpath, index=False)


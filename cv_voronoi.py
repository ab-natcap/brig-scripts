# cv_voronoi.py
# Create Vornoi polygons from CV model points and an outer polygon (like a shoreline buffer)
# Each point is represented by a polygon that does not overlap with any other polygons.

import os
import numpy as np
import geopandas as gpd
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from shapely.geometry import Point
from shapely.ops import cascaded_union


base_dir = '/Users/arbailey/Google Drive/Shared drives/brigBH2021/models/CoastalVulnerability'

# Bahamas-wide with ALL Habitats
# Using Original CV outputs from model
# ce_layer = 'baseline_coastal_exposure_Dec2021'  #'coastal_exposure_all_habitat'
# ce_geopackage = 'coastal_exposure'
# cv_workspace = os.path.join(base_dir, 'CV_outputs', 'CV_outputs_Jan2022_WORKING', 'CV_baseline_v2_Dec2021')

# Using CV layer synthesized by Jess with all habitats and no habitats in MPAs
ce_layer = "CVoutputs_Dec2021_FINAL_NationalScale"
ce_shpfile = ce_layer + ".shp"
cv_workspace = os.path.join(base_dir, 'CV_outputs', 'CV_outputs_Jan2022_WORKING')
ce_shppath = os.path.join(cv_workspace,ce_shpfile)

# scratch_path = os.path.join(base_dir, 'scratch')
# coastal_exposure_gpkg = "{0}/{1}.gpkg".format(cv_workspace, ce_geopackage)
voronoi_gpkg = os.path.join(cv_workspace, 'cv_voronoi.gpkg')
voronoiatt_layer= "{0}_voronoi_att".format(ce_layer)
# Layer to use as the bounding area -- could be a shoreline buffer
outer_bound_poly = '/Volumes/GoogleDrive/Shared drives/brigBH2021/data/work/shoreline/coastline_extract_2km_buffer.shp'
# outer_bound_poly = '/Volumes/GoogleDrive/Shared drives/brigBH2021/data/work/bhs_region.shp'

# print("input geopackage:", coastal_exposure_gpkg)
print("Input Layer: ", ce_layer)
print("output geopackage", voronoi_gpkg)
print("Voronoi + attribute layer:", voronoiatt_layer)
print("Outer boundary or buffer region:", outer_bound_poly)

# ------- Create Vornoi Polygon shapefile from CV coastal exposure point layer ---------------

# Based on
# https://towardsdatascience.com/how-to-create-voronoi-regions-with-geospatial-data-in-python-adbb6c5f2134
# https://github.com/WZBSocialScienceCenter/geovoronoi/blob/master/examples/using_geopandas.py

# Import CV model point data
# cv_points_gdf = gpd.read_file(coastal_exposure_gpkg, layer=ce_layer)
cv_points_gdf = gpd.read_file(os.path.join(cv_workspace, ce_shpfile))
crs = cv_points_gdf.crs

# Convert the pandas Series of Point objects to NumPy array of coordinates
# This creates a 3D point (with Z=0) because source data is Point Z
cv_pt_coords = points_to_coords(cv_points_gdf.geometry)
#  So..... do it this way instead (from Dave's original script)
cv_points = np.array([[x, y] for x, y in zip(cv_points_gdf['geometry'].x, cv_points_gdf['geometry'].y)])

# Import outer boundary / buffer polygon and convert to format for Geovornoi
outer_bound_gdf = gpd.read_file(outer_bound_poly)
outer_bound_shape = cascaded_union(outer_bound_gdf.geometry)

# Create the Voronoi polygons from the points and the outer boundary
print("Creating Voronoi Polygons from: ", ce_layer, " & ", outer_bound_poly)
region_polys, region_pts = voronoi_regions_from_coords(cv_points, outer_bound_shape, per_geom=True)

#  Create a GeoDataFrame with Vornoi Polygon geometries
# vorpolys = gpd.GeoSeries(data=region_polys.values(), index=region_polys.keys(), crs=crs)
vorpolys = gpd.GeoDataFrame(geometry=gpd.GeoSeries(data=region_polys.values()), crs=crs)
# # OUtput to shapefile --- not needed.  Just an intermediate product to check if it works
# print("Output Voronoi Polygons to: ", voronoipoly_path)
# vorpolys.to_file(voronoipoly_path)

# Spatial Join of Voronoi polygons and CV coastal exposure points for attributes
print("Joining Voronoi polygons and CV point attributes")
vor_ce_atts = gpd.sjoin(vorpolys, cv_points_gdf, how='inner', op='contains')
# Output Vornoi Polygons with CV attributes to Geopackage layer
print("output: ", voronoi_gpkg, " | ", voronoiatt_layer)
vor_ce_atts.to_file(voronoi_gpkg, layer=voronoiatt_layer, driver="GPKG")

# Output source CV data to Voronoi Geopackage to have all together
print("output: ", voronoi_gpkg, " | ", ce_layer)
cv_points_gdf.to_file(voronoi_gpkg, layer=ce_layer, driver='GPKG')

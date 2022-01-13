# cv_metrics_vor_pop.py
# Summarize population by CV model points using Vornoi polygons to distribute population raster data

import os
import pandas as pd
import geopandas as gpd
import rasterstats as rs


def zonal_pop_stats(geodf, raster_path, prefix, stat):
    """

    :param geodf:
    :param raster_path:
    :param prefix:
    :param stat:
    :return:
    """
    stats = rs.zonal_stats(geodf, raster_path,
                           geojson_out=True, prefix=prefix,
                           stats=[stat],
                           # all_touched=True
                           )
    statsdf = gpd.GeoDataFrame.from_features(stats)
    summary = statsdf[['shore_id', prefix + stat]].groupby(['shore_id']).sum()
    summary.reset_index(inplace=True)
    return summary



##-----------  MAIN Script ------------------

if __name__ == "__main__":
    # Layers & Paths for input & output data
    base_dir = '/Users/arbailey/Google Drive/Shared drives/brigBH2021/models/CoastalVulnerability'

    # Bahamas-wide with ALL Habitats
    # ce_layer = 'baseline_coastal_exposure_Dec2021'
    # cv_workspace = '../CV_outputs/CVoutputs_AllHabitat_20210830'
    # scratch_path = '../scratch'
    # coastal_exposure_gpkg = "{0}/{1}.gpkg".format(cv_workspace,ce_layer)
    # voronoipoly_path= "{0}/{1}_voronoi.shp".format(scratch_path,ce_layer)
    # voronoiatt_layer= "{0}_voronoi_att".format(ce_layer)

    # -- Baseline -- Countrywide run
    # ce_layer = 'baseline_coastal_exposure_Dec2021'
    # ce_geopackage = 'coastal_exposure'
    # cv_workspace = os.path.join(base_dir, 'CV_outputs', 'CV_outputs_Jan2022_WORKING', 'CV_baseline_v2_Dec2021')
    # Using CV layer synthesized by Jess with all habitats and no habitats in MPAs
    ce_layer = "CVoutputs_Dec2021_FINAL_NationalScale"
    cv_workspace = os.path.join(base_dir, 'CV_outputs', 'CV_outputs_Jan2022_WORKING')
    voronoi_gpkg = os.path.join(cv_workspace, 'cv_voronoi.gpkg')
    voronoiatt_layer = "{0}_voronoi_att".format(ce_layer)

    print("Voronoi geopackage:", voronoi_gpkg)
    print("Voronoi + attribute layer:", voronoiatt_layer)

    # Zonal population stats
    cv_poly = gpd.read_file(voronoi_gpkg, layer=voronoiatt_layer)
    cv_pt = gpd.read_file(voronoi_gpkg, layer=ce_layer)

    pop_dir = os.path.join(base_dir, 'CVinputs_working', 'pop')
    fbd4g_general = os.path.join(pop_dir, 'fbd4g_bhs_general_2020_zeros_32618.tif')
    fbd4g_over60 = os.path.join(pop_dir, 'fbd4g_bhs_elderly_60_plus_2020_zeros_32618.tif')
    fbd4g_under05 = os.path.join(pop_dir, 'fbd4g_bhs_children_under_five_2020_zeros_32618.tif')

    print("Zonal Stats with ", fbd4g_general)
    fbd4g_all_df = zonal_pop_stats(cv_poly, fbd4g_general, 'fbpop_all', 'sum')
    print("Zonal Stats with ", fbd4g_over60)
    fbd4g_over60_df = zonal_pop_stats(cv_poly, fbd4g_over60, 'fbpop_ov60', 'sum')
    print("Zonal Stats with ", fbd4g_under05)
    fbd4g_under05_df = zonal_pop_stats(cv_poly, fbd4g_under05, 'fbpop_und5', 'sum')

    print(fbd4g_all_df)

    print("Combining outputs")
    metrics = pd.concat([fbd4g_all_df, fbd4g_over60_df.iloc[:,-1:], fbd4g_under05_df.iloc[:,-1:]], axis=1)

    print(metrics)
    print(metrics.describe())

    print("Combining voronoi polys with population metrics")
    vornoi_pop_gdf = cv_poly.merge(metrics, on='shore_id')
    print("Combining cv points with population metrics")
    cv_pop_gdf = cv_pt.merge(metrics, on='shore_id')

    # Export
    voronoipop_layer = "{0}_voronoi_pop".format(ce_layer)
    voronoipop_pt_layer = "{0}_vpop_pt".format(ce_layer)
    vornoi_pop_gdf.to_file(voronoi_gpkg, layer=voronoipop_layer, driver="GPKG")
    cv_pop_gdf.to_file(voronoi_gpkg, layer=voronoipop_pt_layer, driver="GPKG")
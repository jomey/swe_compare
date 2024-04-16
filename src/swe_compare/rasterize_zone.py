import numpy as np
import rasterio
import xarray as xr

from rasterio import features
from shapely.geometry import mapping

MASK_NO_ZONE = -999
RASTERIZE_OPTIONS = dict(
    all_touched=True,
    fill=MASK_NO_ZONE,
    dtype=rasterio.int16
)


def rasterize_cbrfc_zone(zone_raster, zone_geometries):
    """
    Convert collection of CBRFC zone into a raster.

    Use rasterio to convert given zone geometries (polygons) into a gridded
    version defined by the given zone raster.

    TODO: Look into replacing with native GDAL
          https://gdal.org/api/python/utilities.html#osgeo.gdal.RasterizeLayer

    Parameters
    ----------
    zone_raster : String
        Path to raster file
    zone_geometries : Iterable
        List of geometries to convert

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    with rasterio.open(zone_raster) as zone_tif:
        transform = zone_tif.transform
        shape = zone_tif.shape

    return features.rasterize(
        zone_geometries,
        transform=transform,
        out_shape=shape,
        **RASTERIZE_OPTIONS
    )


def single_cbrfc_zone_mask(zone_raster, zone_gpd):
    """
    Convert a single CBRFC zone into a raster.

    This will convert the first row of the given geopandas dataframe only.

    Parameters
    ----------
    zone_raster : String
        Path to raster file
    zone_gpd : geopandas dataframe
        Dataframe holding the geometries

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    zone_geometry = [
        (mapping(zone_gpd.iloc[0].geometry), 1)
    ]

    return rasterize_cbrfc_zone(zone_raster, zone_geometry)


def cbrfc_zone_mask(zone_raster, zone_shape):
    zone_geometries = (
        (mapping(geometry), value)
        for geometry, value in zip(
            zone_shape.shapefile.geometry,
            zone_shape.shapefile[zone_shape.ID_COLUMN]
        )
    )

    return rasterize_cbrfc_zone(zone_raster, zone_geometries)


def zone_tif_lons_lats(zone_raster_file):
    with rasterio.open(zone_raster_file) as zone_raster:
        cols, rows = np.meshgrid(
            np.arange(zone_raster.width),
            np.arange(zone_raster.height)
        )
        x, y = rasterio.transform.xy(
            zone_raster.transform, rows, cols
        )

    return np.array(x), np.array(y)


def zone_mask_as_xr(zone_raster, zone_mask):
    lons, lats = zone_tif_lons_lats(zone_raster)

    cbrfc_zones = xr.Dataset({
        "zone": xr.DataArray(
            data=zone_mask,
            dims=['lat', 'lon'],
            coords={
                'lat': (['lat'], lats[:, 0]),
                'lon': (['lon'], lons[0]),
            },
        )
    })
    # Mask no data
    cbrfc_zones = cbrfc_zones.where(cbrfc_zones['zone'] != MASK_NO_ZONE)
    # lat coordinates are flipped for some unknown reason
    return cbrfc_zones.reindex(lat=cbrfc_zones.lat[::-1])


def cbrfc_zone_mask_as_xr(zone_raster, zone_shape):
    zones_mask = cbrfc_zone_mask(zone_raster, zone_shape)
    return zone_mask_as_xr(zone_raster, zones_mask)


def single_cbrfc_zone_mask_as_xr(zone_raster, zone_gpd):
    zones_mask = single_cbrfc_zone_mask(zone_raster, zone_gpd)
    return zone_mask_as_xr(zone_raster, zones_mask)

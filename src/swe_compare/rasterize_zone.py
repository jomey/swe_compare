import numpy as np
import rasterio
import xarray as xr

from rasterio import features
from shapely.geometry import mapping

MASK_NO_ZONE = -999


def cbrfc_zone_mask(zone_raster, zone_shape):
    with rasterio.open(zone_raster) as zone_tif:
        transform = zone_tif.transform
        shape = zone_tif.shape

    zone_geometries = (
        (mapping(geometry), value)
        for geometry, value in zip(
            zone_shape.shapefile.geometry,
            zone_shape.shapefile[zone_shape.ID_COLUMN]
        )
    )

    return features.rasterize(
        zone_geometries,
        transform=transform,
        out_shape=shape,
        all_touched=True,
        fill=MASK_NO_ZONE,
        dtype=rasterio.int16
    )


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


def cbrfc_zone_mask_as_xr(zone_raster, zone_shape):
    zones_mask = cbrfc_zone_mask(zone_raster, zone_shape)
    lons, lats = zone_tif_lons_lats(zone_raster)

    cbrfc_zones = xr.Dataset({
        "zone": xr.DataArray(
            data=zones_mask,
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

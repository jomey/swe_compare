import math
import xarray as xr

from .rasterize_zone import cbrfc_zone_mask_as_xr


def target_bounding_box_padded(target_zones: xr.Dataset) -> dict:
    """
    Get bounding box for Xarray dataset.

    Assumes that the coordinates are labeled as lon/lat. The coordinates
    are also rounded to add padding.

    Parameters
    ----------
    target_zones : xr.Dataset
        Dataset to extract bounding box from.

    Returns
    -------
    dict
        Dictionary containing the lat and lon as keys.
    """
    lon_box = slice(
        math.floor(target_zones.lon.values.min()),
        math.ceil(target_zones.lon.values.max())
    )
    lat_box = slice(
        math.floor(target_zones.lat.values.min()),
        math.ceil(target_zones.lat.values.max())
    )
    return dict(lat=lat_box, lon=lon_box)


def combine_cbrfc_swann(swann, cbrfc_zones):
    """
    Combines CBRFC mask with SWANN SWE and
    computes the CBRFC zonal mean.
    """
    return xr.combine_by_coords(
        [
            cbrfc_zones,
            swann,
        ],
        coords=['lat', 'lon'],
        join='inner'
    ).groupby('zone').mean()


def swann_swe_for_zones(
    swann_files,
    cbrfc_zone_tif,
    cbrfc_zone_shape,
    target_zones_dict,
):
    """
    Mask SWANN SWE with given CBRFC zone Tif and list of
    targeted zones.
    """

    target_cbrfc_zones = cbrfc_zone_mask_as_xr(
        cbrfc_zone_tif, cbrfc_zone_shape
    )

    # Reduce to zones of interest
    target_cbrfc_zones = target_cbrfc_zones.where(
        target_cbrfc_zones.isin(list(target_zones_dict.values())),
        drop=True
    )

    # Get SWE values for bounding box of target zones
    swann = xr.open_mfdataset(swann_files, parallel=True).sel(
        target_bounding_box_padded(target_cbrfc_zones)
    )

    swann = swann.interp(
        lat=target_cbrfc_zones.lat.values,
        lon=target_cbrfc_zones.lon.values,
        method='nearest'
    )

    swann_cbrfc_zones = combine_cbrfc_swann(swann, target_cbrfc_zones)

    return swann_cbrfc_zones.where(
        swann_cbrfc_zones.zone.isin(
            list(target_zones_dict.values())
        ), drop=True
    ).SWE.compute()

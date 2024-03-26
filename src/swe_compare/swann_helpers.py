import xarray as xr

from .rasterize_zone import cbrfc_zone_mask_as_xr


def combine_cbrfc_swann(swann_files, cbrfc_zones):
    """
        Combines CBRFC mask with SWANN SWE and 
        computes the CBRFC zonal mean.
    """
    return xr.combine_by_coords(
        [
            xr.open_mfdataset(swann_files, parallel=True),
            cbrfc_zones
        ], 
        coords=['lat', 'lon'], 
        join='override'
    ).groupby('zone').mean()


def swann_swe_for_zones(
    swann_files, 
    cbrfc_zone_tif,
    cbrfc_zone_shape,
    target_zones_dict
):
    cbrfc_zones = cbrfc_zone_mask_as_xr(cbrfc_zone_tif, cbrfc_zone_shape)
    swann_cbrfc_zones = combine_cbrfc_swann(swann_files, cbrfc_zones)
    return swann_cbrfc_zones.where(
        swann_cbrfc_zones.zone.isin(
            list(target_zones_dict.values())
        ), drop=True
    ).SWE.compute()

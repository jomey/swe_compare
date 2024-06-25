import xarray as xr

from swed_17.nb_helpers import start_cluster
from swed_17 import Snow17SWE, ZoneCompare, ZoneDB, ZonePlotter
from swed_17.peak_swe import peak_swe_for_pd, plot_peak_swe_pd, compare_peak_swe
from swed_17.swann_helpers import swann_data_for_zone, swann_swe_for_zone, peak_swe_for_swann

# Plotting
import holoviews as hv
import hvplot.xarray
import hvplot.pandas
import matplotlib.pyplot as plt

BOKEH_OPTS = dict(
    width=900,
    height=600,
    cmap='viridis',
)

hv.plotting.bokeh.ElementPlot.active_tools = [
    'save', 'pan', 'box_zoom', 'reset'
]

# Jupyter Lab has missing PROJ envs
import os
os.environ['PROJ_DATA'] = '/perc10/data/miniconda3/envs/snow_viz/share/proj'

# Create a nb_paths.py file that holds all directory infos
# This is not commited with the repository
# List of needed variables:
## CBRFC zones
#  * ZONE_DIR
#  * GSL_ZONES
#  * UC_ZONES
#  * LC_ZONES
## CBRFC zones as tif
#  * ZONE_TIF_DIR
#  * GSL_ZONE_TIF
#  * UC_ZONE_TIF
#  * LC_ZONE_TIF
## SWE files
#  * SWE_HOME_DIR
## SWANN files
#  * SWANN_HOME_DIR
from nb_paths import *

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

# Interactive HTML pages
import panel as pn
from bokeh.resources import INLINE

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

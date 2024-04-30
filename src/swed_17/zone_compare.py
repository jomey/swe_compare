import holoviews as hv
import pandas as pd
import panel as pn
import xarray as xr

from bokeh.resources import INLINE


class ZoneCompare:
    """
    Generate time series and scatter plot for two datasets.
    """

    def __init__(
        self,
        zone_name: str,
        snow_17: pd.Series,
        swann: xr.DataArray,
        year_range: range
    ):
        """
        Parameters
        ----------
        zone_name : str
            Zone name for plot title
        snow_17 : pd.Series
            Snow 17 data
        swann : xr.DataArray
            SWANN data
        year_range : range
            Range of years for correlation analysis
        """
        self.zone_name = zone_name
        self.snow_17 = snow_17
        self.swann = swann
        self.year_range = pd.to_datetime(
            [f'{year}-03-01' for year in year_range]
        )

    def correlation_plot(self) -> hv.Layout:
        """
        Scatter plot with a 1:1 line

        Returns
        -------
        hv.Layout
        """
        axes_limits = (-20, 1000)

        # Get requested date range
        snow_17 = self.snow_17.loc[self.year_range]
        # Convert to use pandas correlation functions
        swann = self.swann.sel(time=self.year_range).to_pandas()

        # Calculate R^2
        correlation_r2 = str(
            f'{snow_17.corr(swann):.3}'
        )

        return hv.Overlay([
            hv.Slope(1, 0).opts(color='orange'),
            hv.Scatter(
                list(zip(snow_17, swann))
            ).opts(
                xlim=axes_limits, ylim=axes_limits,
                title=f'{self.zone_name} - March 1st SWE',
                xlabel='CBRFC SWE (mm)',  ylabel='SWANN SWE (mm)',
                color='k', size=10,
                width=500, height=500
            ) * hv.Text(300, 10, correlation_r2),
        ])

    def time_series_plot(self) -> hv.Overlay:
        """
        Create time series plot overlaying both datasets

        Returns
        -------
        hv.Overlay
        """
        return hv.Overlay([
            self.snow_17.hvplot().opts(
                ylim=(-20, None),
                title=self.zone_name, ylabel='SWE (mm)',
                width=1200, height=600,
            ),
            self.swann.hvplot('time', label='SWANN')
        ])

    def plot_all(self) -> hv.Layout:
        """
        Plot the time series and correlation side-by-side

        Returns
        -------
        hv.Layout
        """
        return hv.Layout(
            self.time_series_plot() + self.correlation_plot()
        ).cols(2)

    @classmethod
    def show_all(cls, collection: list) -> hv.Layout:
        """
        Show collection of zone compare instances in one layout with two columns.

        For use in notebooks.

        Parameters
        ----------
        collection : list
            Collection of ZoneCompare instances

        Returns
        -------
        hv.Layout
            Holoviews layout with all plots
        """
        plots = [zone_compare.plot_all() for zone_compare in collection]
        return hv.Layout(plots).opts(shared_axes=False).cols(2)

    @classmethod
    def save_html(cls, file_path: str, collection: list) -> None:
        """
        Save plots as interactive HTML page

        Parameters
        ----------
        file_path : str
            Path to save files to
        collection : list
            Collection of ZoneCompare instances
        """

        pn.pane.HoloViews(
            cls.show_all(collection)
        ).save(
            file_path, embed=True, resources=INLINE
        )

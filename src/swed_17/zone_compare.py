import holoviews as hv
import hvplot.pandas    # noqa
import pandas as pd
import xarray as xr

from .peak_swe import peak_swe_for_pd

class ZoneCompare:
    """
    Generate time series and scatter plot for two datasets.
    """

    def __init__(
        self,
        zone_name: str,
        snow_17: pd.Series,
        swann: pd.DataFrame
    ):
        """
        Parameters
        ----------
        zone_name : str
            Zone name for plot title
        snow_17 : pd.Series
            Snow 17 data
        swann : pd.DataFrame
            SWANN data
        """
        self.zone_name = zone_name
        self.snow_17 = snow_17.to_frame()
        self.swann = swann

    def correlation_plot(self) -> hv.Layout:
        """
        Scatter plot with a 1:1 line on dates of peak SWE per year

        Returns
        -------
        hv.Layout
        """
        axes_limits = (-20, 1000)

        snow_17_peak_swe_dates = peak_swe_for_pd(self.snow_17, False)
        # Ensure that early years are present in SWANN
        snow_17_peak_swe_dates = snow_17_peak_swe_dates[
            snow_17_peak_swe_dates[self.zone_name] > self.swann.index[0]
        ]

        peak_swe_values = self.snow_17.loc[
            snow_17_peak_swe_dates[self.zone_name].values
        ].join(
            self.swann.loc[
                snow_17_peak_swe_dates[self.zone_name].values
            ]
        )

        # Calculate R^2
        correlation_r2 = str(
            f'{peak_swe_values.corr().values[0, 1]:.3}'
        )

        return peak_swe_values.hvplot.scatter().opts(
                title=f'{self.zone_name} - Peak SWE values',
                width=800, height=500
            ) + hv.Table({'R-square': [correlation_r2]}, 'R-square').opts(title='Peak SWE')


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
            self.swann.hvplot(label='SWANN')
        ])

    def plot(self) -> hv.Layout:
        """
        Plot the time series and correlation side-by-side

        Returns
        -------
        hv.Layout
        """
        return hv.Layout(
            self.time_series_plot() + self.correlation_plot()
        ).cols(2)

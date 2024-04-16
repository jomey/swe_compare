import holoviews as hv
import pandas as pd
import panel as pn

from bokeh.resources import INLINE


class ZoneCompare:
    def __init__(self, target_zones, cbrfc_swe, swann_swe, year_range):
        self.target_zones = target_zones
        self.cbrfc_swe = cbrfc_swe
        self.swann_swe = swann_swe
        self.year_range = pd.to_datetime(
            [f'{year}-03-01' for year in year_range]
        )

    def plot_panels(self, name):
        zone_ID = self.target_zones[name]
        axes_limits = (-20, 1000)

        swann_data = self.swann_swe.sel(zone=zone_ID)

        snow_17_m1 = self.cbrfc_swe.loc[self.year_range][name].values
        swann_m1 = swann_data.loc[self.year_range].values

        correlation = str(
            f'{pd.Series(snow_17_m1).corr(pd.Series(swann_m1)):.3}'
        )

        scatter = hv.Overlay([
            hv.Slope(1, 0).opts(color='orange'),
            hv.Scatter(
                list(zip(snow_17_m1, swann_m1))
            ).opts(
                xlim=axes_limits, ylim=axes_limits,
                title=f'{name} - March 1st SWE',  xlabel='CBRFC SWE (mm)',  ylabel='SWANN SWE (mm)',
                color='k', size=10,
                width=500, height=500
            ) * hv.Text(300, 10, correlation),
        ])
        time_series = hv.Overlay([
            self.cbrfc_swe[name].hvplot().opts(
                ylim=(-20, None),
                title=name, ylabel='SWE (mm)',
                width=1200, height=600,
            ),
            swann_data.hvplot('time', label=f'SWANN')
        ])
        return hv.Layout(time_series + scatter).cols(1)

    def show_all(self):
        plots = [self.plot_panels(zone) for zone in self.target_zones.keys()]
        return hv.Layout(plots).opts(shared_axes=False).cols(2)

    def save_html(self, file_path):
        """
        Save plots as interactive HTML page
        """
        pn.pane.HoloViews(
            self.show_all()
        ).save(
            file_path, embed=True, resources=INLINE
        )

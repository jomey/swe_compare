"""
Functions to extract and plot peak snow water equivalent date (SWE) from
pandas Dataframes
"""

import pandas as pd
import holoviews as hv
import hvplot.pandas    # noqa

from bokeh.models import DatetimeTickFormatter, HoverTool


def peak_swe_for_zone(
        swe_data: pd.DataFrame, zone: str, year_range: range
) -> list:
    """
    Get the date of peak SWE from a Dataframe and in given zone and year range.

    The year of each date will be changed to be 1880 to be able to compare each
    year. To get the actual year of the value, use the Dataframe index.

    Parameters
    ----------
    swe_data : pd.DataFrame
        Data to search through
    zone : str
        CBRFC zone name
    year_range : range
        Year range to get dates for

    Returns
    -------
    list
        Peak SWE dates for each year.
    """
    peaks = [
        swe_data[zone].loc[f"{year - 1}-10-01":f"{year}-09-30"].idxmax()
        for year in year_range
    ]

    # Modify each year to the leap year in 1880
    return [date.replace(year=1880) for date in peaks]


def peak_swe_for_pd(swe_data: pd.DataFrame) -> pd.DataFrame:
    """
    Get the date of peak SWE for each zone in the Dataframe.

    Each column is assumed to hold the SWE data and the column label being the
    zone name

    Parameters
    ----------
    swe_data : pd.DataFrame
        Data to search through

    Returns
    -------
    pd.DataFrame
        Peak SWE date for each year and zone
    """

    year_range = range(
        (swe_data.index.min().year + 1),
        swe_data.index.max().year
    )

    peak_swe = pd.DataFrame.from_dict({
        'year': year_range,
    })

    for zone in swe_data.columns.values:
        peak_swe[zone] = peak_swe_for_zone(swe_data, zone, year_range)

    peak_swe = peak_swe.set_index('year')

    return peak_swe


def plot_peak_swe_pd(swe_data: pd.DataFrame, title: str = '') -> hv.Overlay:
    """
    Plot dataframe from :meth:`peak_swe_for_pd` interactively with Bokeh.

    Parameters
    ----------
    swe_data : pd.DataFrame
        Data to plot
    title : str
        Plot title

    Returns
    -------
    hv.Overlay
        Holoviews plot
    """
    return swe_data.hvplot(
        tools=[
            HoverTool(
                tooltips=[
                    ("zone", "$name"),
                    ("year", "WY-@year"),
                    ("date", "@value{%m/%d}"),
                ],
                formatters={
                    "@value": "datetime",
                },
            )
        ]
    ).opts(
        title=title,
        yformatter=DatetimeTickFormatter(months="%m/%d"),
        ylabel='Month/Day',
        width=900,
        height=600,
    )


def compare_peak_swe(
        cbrfc_swe: pd.DataFrame, swann_swe: dict
) -> list:
    """Create comparison plot for peak SWE dates in given dataframes.

    The cbrfc_swe column names will be used to match the key in swann_swe
    dictionary.

    Parameters
    ----------
    cbrfc_swe : pd.DataFrame
        Peak SWE dates for CBRFC
    swann_swe : dict
        Peak SWE dates for SWANN zones.

    Returns
    -------
    list
        Holoviews overlays for each zone
    """
    return [
        plot_peak_swe_pd(
            cbrfc_swe[key].to_frame().join(swann_swe[key]),
            "Peak SWE - " + key
        ) for key in cbrfc_swe.columns.values
    ]

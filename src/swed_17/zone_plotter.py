import holoviews as hv
import panel as pn

from bokeh.resources import INLINE


class ZonePlotter:
    """
    Utility class for plotting and export to HTML pages
    """
    @classmethod
    def show_all(cls, collection: list, columns: int = 2) -> hv.Layout:
        """
        Show given collection in one layout with given columns number.

        For use in notebooks.

        Parameters
        ----------
        collection : list
            Collection of Holoview plots
        columns: int
            Number of columns in the layout. (Default: 2)

        Returns
        -------
        hv.Layout
            Holoviews layout with all plots in two columns
        """
        return hv.Layout(collection).opts(shared_axes=False).cols(columns)

    @classmethod
    def save_html(
        cls, file_path: str, collection: list, columns: int = 2
    ) -> None:
        """
        Save plots as interactive HTML page

        Parameters
        ----------
        file_path : str
            Path to save files to
        collection : list
            Collection of ZoneCompare instances
        columns : int
            Number of columns in the layout.
        """

        collection = cls.show_all(collection, columns)

        pn.pane.HoloViews(
            collection
        ).save(
            file_path, embed=True, resources=INLINE
        )

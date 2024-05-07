import holoviews as hv
import panel as pn

from bokeh.resources import INLINE


class ZonePlotter:
    """
    Utility class for plotting and export to HTML pages
    """
    @classmethod
    def show_all(cls, collection: list) -> hv.Layout:
        """
        Show given collection in one layout with two columns.

        For use in notebooks.

        Parameters
        ----------
        collection : list
            Collection of Holoview plots

        Returns
        -------
        hv.Layout
            Holoviews layout with all plots in two columns
        """
        return hv.Layout(collection).opts(shared_axes=False).cols(2)

    @classmethod
    def save_html(
        cls, file_path: str, collection: list, two_cols: bool = True
    ) -> None:
        """
        Save plots as interactive HTML page

        Parameters
        ----------
        file_path : str
            Path to save files to
        collection : list
            Collection of ZoneCompare instances
        two_cols : bool
            Indicate plot layout. 'True' creates two columns (Default) and
            'False' has one.
        """

        if two_cols:
            collection = cls.show_all(collection)

        pn.pane.HoloViews(
            collection
        ).save(
            file_path, embed=True, resources=INLINE
        )

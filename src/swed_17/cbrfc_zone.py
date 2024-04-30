import geopandas as gpd
import hvplot.pandas


class CBRFCZone:
    ID_COLUMN = 'mask_ID'

    def __init__(self, shapefile):
        self._shapefile = gpd.read_file(shapefile)
        self.assign_zone_id()

    @property
    def shapefile(self):
        return self._shapefile

    def assign_zone_id(self):
        """
            Give each zone a unique ID as basis for a zone mask
        """
        self._shapefile[self.ID_COLUMN] = range(0, len(self._shapefile))

    def target_zones_as_dict(self, target_zones):
        return {
            record['zone']: record[self.ID_COLUMN]
            for record in self.shapefile.query("zone in @target_zones")[
                ["zone", self.ID_COLUMN]
            ].to_dict('records')
        }

    def explore_zones(self):
        return self._shapefile.explore(popup=['zone', 'mask_ID'])

    def plot_zones(self):
        return self.shapefile.hvplot(
            c='mask_ID', color_key='Category10'
        ).opts(width=900, height=600)

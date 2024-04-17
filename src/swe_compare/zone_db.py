import psycopg

from psycopg.rows import Row
from rasterio.io import MemoryFile


class ZoneDB:
    """
Database query class.
    """
    COORDS_CONVERSION = {'x': 'lon', 'y': 'lat'}

    class Query:
        """
        Set of pre-defined database queries.
        """
        ZONE_AS_RASTER = "SELECT ST_AsGDALRaster(ST_Union(zone_mask.rast), 'GTiff') " \
                         "FROM zone_mask_as_raster(%(zone_name)s) AS zone_mask"

    def __init__(self, connection_info: str):
        self._connection_info = connection_info
        self.connection = psycopg.connect(
            connection_info, autocommit=True
        )

    def query(self, query: str, params: dict = {}) -> Row:
        """
        Execute given query by passing in requested parameters

        Parameters
        ----------
        query : str
            SQL query
        params : dict, optional
            Pass in query parameters if the query contains any, by default {}

        Returns
        -------
        Row
            Query result as psycopg row.
        """
        with self.connection as connection:
            with connection.cursor() as curs:
                curs.execute(query, params)
                return curs.fetchone()

    def zone_as_rio(self, zone_name: str) -> MemoryFile:
        """
        Query for a zone mask and return as a rasterio MemoryFile.

        Parameters
        ----------
        zone_name : str
            SQL query

        Returns
        -------
        MemoryFile
            Result of query as rasterio MemoryFile
        """
        result = self.query(
            self.Query.ZONE_AS_RASTER, {'zone_name': zone_name}
        )
        return MemoryFile(bytes(result[0]))

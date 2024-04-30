import pandas as pd


class Snow17SWE:
    """
    Parse CSV file into a pandas data frame.

    The assumed structure of the file is:
    year,month,day,ztime,ZONE_NAME1,ZONE_NAME2,...

    """
    INCH_TO_MM = 25.4
    DTYPES = {
        'year': str, 'month': str, 'day': str
    }
    DATE_INDEX_FORMAT = '%Y-%m-%d'

    def __init__(self, swe_csv):
        self._csv = pd.read_csv(
            swe_csv, header=0, dtype=self.DTYPES
        )
        self.create_time_index()
        self.swe_to_mm()

    @property
    def csv(self) -> pd.DataFrame:
        """
        Get the parsed CSV file data frame.

        Returns
        -------
        pd.DataFrame
        """
        return self._csv

    def create_time_index(self) -> None:
        """
        Concatenate the date columns (year, month, day) and set as index on
        the dataframe. This also removes the 'ztime' column
        """
        self._csv['Date'] = pd.to_datetime(
            self.csv.pop('year') + '-' + self.csv.pop('month') +
            '-' + self.csv.pop('day'),
            format=self.DATE_INDEX_FORMAT
        )

        self._csv = self.csv.drop('ztime', axis=1).set_index('Date')

    def swe_to_mm(self) -> None:
        """
        Convert all columns from inces to mm.
        """
        for key in self.csv.columns:
            self.csv[key] *= self.INCH_TO_MM

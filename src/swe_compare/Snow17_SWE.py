import pandas as pd


class Snow17SWE:
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
    def csv(self):
        return self._csv

    def create_time_index(self):
        self._csv['Date'] = pd.to_datetime(
            self.csv.pop('year') + '-' + self.csv.pop('month') +
            '-' + self.csv.pop('day'),
            format=self.DATE_INDEX_FORMAT
        )

        self._csv = self.csv.drop('ztime', axis=1).set_index('Date')

    def swe_to_mm(self):
        for key in self.csv.columns:
            self.csv[key] *= self.INCH_TO_MM

import csv
import datetime


class Row(dict):

    def __init__(self, *args, **kwargs):
        super(Row, self).__init__(*args, **kwargs)
        self._date_issued = None

    @property
    def date_issued(self):
        if self._date_issued is None:
            self._date_issued = datetime.datetime.strptime(
                self['DATE ISSUED'],
                '%m/%d/%Y',
            ).date()
        return self._date_issued

    @property
    def account_number(self):
        return self['ACCOUNT NUMBER']


class RawReader(csv.DictReader):

    def __iter__(self, *args, **kwargs):
        row = self.next()
        while row:
            yield Row(row)
            row = self.next()


class RawWriter(csv.DictWriter):
    pass

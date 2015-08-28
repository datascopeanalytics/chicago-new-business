import csv
import datetime


class Row(dict):

    def __init__(self, *args, **kwargs):
        super(Row, self).__init__(*args, **kwargs)
        self._start_date = None
        self._end_date = None

    def _cast_date(self, s):
        if not s:
            return None
        return datetime.datetime.strptime(s, '%m/%d/%Y').date()

    def _get_date_or_cast(self, s, attr):
        if getattr(self, attr) is None:
            setattr(self, attr, self._cast_date(s))
        return getattr(self, attr)

    @property
    def start_date(self):
        return self._get_date_or_cast(
            self['DATE ISSUED'],
            '_start_date',
        )

    @property
    def end_date(self):
        return self._get_date_or_cast(
            self['LICENSE TERM EXPIRATION DATE'],
            '_end_date',
        )

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

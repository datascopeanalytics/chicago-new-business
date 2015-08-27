import csv
import datetime


class Row(dict):

    def __init__(self, *args, **kwargs):
        super(Row, self).__init__(*args, **kwargs)
        self._date_issued = None
        self._expiration_date = None

    def _cast_date(self, s):
        if not s:
            return None
        return datetime.datetime.strptime(s, '%m/%d/%Y').date()

    def _get_date_or_cast(self, s, attr):
        if getattr(self, attr) is None:
            setattr(self, attr, self._cast_date(s))
        return getattr(self, attr)

    @property
    def date_issued(self):
        return self._get_date_or_cast(
            self['DATE ISSUED'],
            '_date_issued',
        )

    @property
    def expiration_date(self):
        return self._get_date_or_cast(
            self['LICENSE TERM EXPIRATION DATE'],
            '_expiration_date',
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

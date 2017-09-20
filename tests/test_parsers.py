from datetime import datetime, date, time, timedelta, timezone
from unittest import TestCase
from lie2me.parsers import parse_datetime, parse_date, parse_time, parse_timezone


class DateTimeParserTestCase(TestCase):

    def test_valid_naive_datetimes(self):
        self.assertEqual(parse_datetime('2017-09-20 09'), datetime(2017, 9, 20, 9))
        self.assertEqual(parse_datetime('2017-09-20 19'), datetime(2017, 9, 20, 19))
        self.assertEqual(parse_datetime('2017-09-20T19'), datetime(2017, 9, 20, 19))
        self.assertEqual(parse_datetime('2017-09-20 19:34'), datetime(2017, 9, 20, 19, 34))
        self.assertEqual(parse_datetime('2017-09-20 19:34:59'), datetime(2017, 9, 20, 19, 34, 59))
        self.assertEqual(parse_datetime('2017-09-20T19:34:59'), datetime(2017, 9, 20, 19, 34, 59))

    def test_unusual_valid_inputs(self):
        self.assertEqual(parse_datetime('  2017-09-20    19:34  '), datetime(2017, 9, 20, 19, 34))
        self.assertEqual(parse_datetime('2017-09-20 T 19:34'), datetime(2017, 9, 20, 19, 34))

    def test_invalid_inputs(self):
        self.assertEqual(parse_datetime(None), None)
        self.assertEqual(parse_datetime([]), None)
        self.assertEqual(parse_datetime(''), None)
        self.assertEqual(parse_datetime('foobar'), None)

    def test_invalid_naive_datetimes(self):
        self.assertEqual(parse_datetime('2017'), None)
        self.assertEqual(parse_datetime('2017-09-20'), None)
        self.assertEqual(parse_datetime('2017-09-2019:34'), None)
        self.assertEqual(parse_datetime('2017-02-30 19:34'), None)
        self.assertEqual(parse_datetime('2017-09-20-19:34'), None)
        self.assertEqual(parse_datetime('2017-09-20 19:345'), None)
        self.assertEqual(parse_datetime('2017-09-20 19:34:'), None)
        self.assertEqual(parse_datetime('2017-09-20 19:34:000'), None)

    def test_valid_aware_datetimes(self):
        self.assertEqual(parse_datetime('2017-09-20 19:47:35Z'), self.aware_datetime(2017, 9, 20, 19, 47, 35, offset=0))
        self.assertEqual(parse_datetime('2017-09-20 19:47:35-03:00'), self.aware_datetime(2017, 9, 20, 19, 47, 35, offset=-3))
        self.assertEqual(parse_datetime('2017-09-20 19:47:35-0300'), self.aware_datetime(2017, 9, 20, 19, 47, 35, offset=-3))
        self.assertEqual(parse_datetime('2017-09-20 19:47:35-03'), self.aware_datetime(2017, 9, 20, 19, 47, 35, offset=-3))
        self.assertEqual(parse_datetime('2017-09-20 19:47-03'), self.aware_datetime(2017, 9, 20, 19, 47, offset=-3))
        self.assertEqual(parse_datetime('2017-09-20 19-03'), self.aware_datetime(2017, 9, 20, 19, offset=-3))
        self.assertEqual(parse_datetime('2017-09-20 19Z'), self.aware_datetime(2017, 9, 20, 19, offset=0))
        self.assertEqual(parse_datetime('2017-09-20T19Z'), self.aware_datetime(2017, 9, 20, 19, offset=0))

    def aware_datetime(self, year, month, day, hour, minute=0, second=0, microsecond=0, offset=0):
        dt = datetime(year, month, day, hour, minute, second, microsecond)
        return dt.replace(tzinfo=timezone(timedelta(hours=offset)))

    def test_invalid_aware_datetimes(self):
        self.assertEqual(parse_datetime('2017-09-20 19:47:35ZZ'), None)
        self.assertEqual(parse_datetime('2017-09-20 19:47:35-3:00'), None)
        self.assertEqual(parse_datetime('2017-09-20 19:47:35-030'), None)
        self.assertEqual(parse_datetime('2017-09-20 19:47:35-3'), None)
        self.assertEqual(parse_datetime('2017-09-20 -03'), None)
        self.assertEqual(parse_datetime('2017-09-20 19-3'), None)
        self.assertEqual(parse_datetime('2017-09-2019Z'), None)
        self.assertEqual(parse_datetime('2017-09-20T19-'), None)


class DateParserTestCase(TestCase):

    def test_valid_date(self):
        self.assertEqual(parse_date('2017-09-20'), date(2017, 9, 20))
        self.assertEqual(parse_date('2017-9-2'), date(2017, 9, 2))

    def test_invalid_dates(self):
        self.assertEqual(parse_date(None), None)
        self.assertEqual(parse_date([]), None)
        self.assertEqual(parse_date(''), None)
        self.assertEqual(parse_date('30'), None)
        self.assertEqual(parse_date('09-30'), None)
        self.assertEqual(parse_date('2017-02-30'), None)
        self.assertEqual(parse_date('2017-09--20'), None)
        self.assertEqual(parse_date('2017-09-200'), None)
        self.assertEqual(parse_date('2017-09'), None)
        self.assertEqual(parse_date('2017'), None)


class TimeParserTestCase(TestCase):

    def test_valid_naive_times(self):
        self.assertEqual(parse_time('08:30:59'), time(8, 30, 59))
        self.assertEqual(parse_time('00:00:00'), time(0))
        self.assertEqual(parse_time('08:30'), time(8, 30))
        self.assertEqual(parse_time('08'), time(8))
        self.assertEqual(parse_time('08:30.999'), time(8, 30, 0, 999000))

    def test_invalid_inputs(self):
        self.assertEqual(parse_time(None), None)
        self.assertEqual(parse_time([]), None)
        self.assertEqual(parse_time(''), None)

    def test_invalid_naive_times(self):
        self.assertEqual(parse_time('8'), None)
        self.assertEqual(parse_time('24'), None)
        self.assertEqual(parse_time('08:'), None)
        self.assertEqual(parse_time('08:0'), None)
        self.assertEqual(parse_time('23:60'), None)
        self.assertEqual(parse_time('23-60'), None)
        self.assertEqual(parse_time('08:00:0'), None)
        self.assertEqual(parse_time('08:00:60'), None)
        self.assertEqual(parse_time('08:00:59.'), None)
        self.assertEqual(parse_time('08:00:59.9999'), None)

    def test_valid_aware_times(self):
        self.assertEqual(parse_time('08Z'), self.aware_time(8, offset=0))
        self.assertEqual(parse_time('08:30Z'), self.aware_time(8, 30, offset=0))
        self.assertEqual(parse_time('08:30:59Z'), self.aware_time(8, 30, 59, offset=0))
        self.assertEqual(parse_time('08-03:00'), self.aware_time(8, offset=-3))
        self.assertEqual(parse_time('08-0300'), self.aware_time(8, offset=-3))
        self.assertEqual(parse_time('08-03'), self.aware_time(8, offset=-3))
        self.assertEqual(parse_time('08:30-03:00'), self.aware_time(8, 30, offset=-3))
        self.assertEqual(parse_time('08:30-0300'), self.aware_time(8, 30, offset=-3))
        self.assertEqual(parse_time('08:30-03'), self.aware_time(8, 30, offset=-3))
        self.assertEqual(parse_time('08:30:59-03:00'), self.aware_time(8, 30, 59, offset=-3))
        self.assertEqual(parse_time('08:30:59-0300'), self.aware_time(8, 30, 59, offset=-3))
        self.assertEqual(parse_time('08:30:59-03'), self.aware_time(8, 30, 59, offset=-3))
        self.assertEqual(parse_time('08:30:59-23:00'), self.aware_time(8, 30, 59, offset=-23))
        self.assertEqual(parse_time('08+03:00'), self.aware_time(8, offset=3))
        self.assertEqual(parse_time('08+0300'), self.aware_time(8, offset=3))
        self.assertEqual(parse_time('08+03'), self.aware_time(8, offset=3))
        self.assertEqual(parse_time('08:30+03:00'), self.aware_time(8, 30, offset=3))
        self.assertEqual(parse_time('08:30+0300'), self.aware_time(8, 30, offset=3))
        self.assertEqual(parse_time('08:30+03'), self.aware_time(8, 30, offset=3))
        self.assertEqual(parse_time('08:30:59+03:00'), self.aware_time(8, 30, 59, offset=3))
        self.assertEqual(parse_time('08:30:59+0300'), self.aware_time(8, 30, 59, offset=3))
        self.assertEqual(parse_time('08:30:59+03'), self.aware_time(8, 30, 59, offset=3))
        self.assertEqual(parse_time('08:30:59+23:00'), self.aware_time(8, 30, 59, offset=23))

    def aware_time(self, hour, minute=0, second=0, microsecond=0, offset=0):
        tm = time(hour, minute, second, microsecond)
        return tm.replace(tzinfo=timezone(timedelta(hours=offset)))

    def test_invalid_aware_times(self):
        self.assertEqual(parse_time('08:30-3'), None)
        self.assertEqual(parse_time('08:30-03:'), None)
        self.assertEqual(parse_time('08:30-03:00:'), None)
        self.assertEqual(parse_time('08:30-03:00:00'), None)
        self.assertEqual(parse_time('08:30-24:00'), None)
        self.assertEqual(parse_time('08:30+24:00'), None)


class TimeZoneParserTestCase(TestCase):

    def test_valid_utc_timezone(self):
        self.assertEqual(parse_timezone('Z'), timedelta(0))
        self.assertEqual(parse_timezone('+00'), timedelta(0))
        self.assertEqual(parse_timezone('+00:00'), timedelta(0))
        self.assertEqual(parse_timezone('+0000'), timedelta(0))

    def test_invalid_utc_timezones(self):
        self.assertEqual(parse_timezone('z'), None)
        self.assertEqual(parse_timezone('+0'), None)
        self.assertEqual(parse_timezone('+000'), None)
        self.assertEqual(parse_timezone('+00000'), None)
        self.assertEqual(parse_timezone('-00'), None)
        self.assertEqual(parse_timezone('-0000'), None)

    def test_valid_timezones(self):
        self.assertEqual(parse_timezone('-03'), timedelta(hours=-3))
        self.assertEqual(parse_timezone('-00:30'), timedelta(minutes=-30))
        self.assertEqual(parse_timezone('-0030'), timedelta(minutes=-30))
        self.assertEqual(parse_timezone('-03:00'), timedelta(hours=-3))
        self.assertEqual(parse_timezone('-03:35'), timedelta(hours=-3, minutes=-35))
        self.assertEqual(parse_timezone('-0300'), timedelta(hours=-3))
        self.assertEqual(parse_timezone('-23'), timedelta(hours=-23))
        self.assertEqual(parse_timezone('-23:59'), timedelta(hours=-23, minutes=-59))
        self.assertEqual(parse_timezone('-2359'), timedelta(hours=-23, minutes=-59))
        self.assertEqual(parse_timezone('+03'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+00:30'), timedelta(minutes=30))
        self.assertEqual(parse_timezone('+0030'), timedelta(minutes=30))
        self.assertEqual(parse_timezone('+03:00'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+03:35'), timedelta(hours=3, minutes=35))
        self.assertEqual(parse_timezone('+0300'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+0300'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+23'), timedelta(hours=23))
        self.assertEqual(parse_timezone('+23:59'), timedelta(hours=23, minutes=59))
        self.assertEqual(parse_timezone('+2359'), timedelta(hours=23, minutes=59))

    def test_invalid_timezones(self):
        self.assertEqual(parse_timezone(None), None)
        self.assertEqual(parse_timezone('-3'), None)
        self.assertEqual(parse_timezone('-03:'), None)
        self.assertEqual(parse_timezone('-03:00:'), None)
        self.assertEqual(parse_timezone('-03:00:00'), None)
        self.assertEqual(parse_timezone('-24:00'), None)
        self.assertEqual(parse_timezone('+24:00'), None)
        self.assertEqual(parse_timezone('-25:00'), None)
        self.assertEqual(parse_timezone('+25:00'), None)

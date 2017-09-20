from datetime import time, timedelta, timezone
from unittest import TestCase
from lie2me.parsers import parse_time, parse_timezone


class TimeParserTestCase(TestCase):

    def aware_time(self, hour, minute=0, second=0, microsecond=0, offset=0):
        tm = time(hour, minute, second, microsecond)
        return tm.replace(tzinfo=timezone(timedelta(hours=offset)))

    def test_valid_naive_times(self):
        self.assertEqual(parse_time('08:30:59'), time(8, 30, 59))
        self.assertEqual(parse_time('00:00:00'), time(0))
        self.assertEqual(parse_time('08:30'), time(8, 30))
        self.assertEqual(parse_time('08'), time(8))
        self.assertEqual(parse_time('08:30.999'), time(8, 30, 0, 999000))

    def test_invalid_naive_times(self):
        with self.assertRaises(TypeError):
            parse_time(None)
        with self.assertRaises(ValueError):
            parse_time('')
        with self.assertRaises(ValueError):
            parse_time('8')
        with self.assertRaises(ValueError):
            parse_time('24')
        with self.assertRaises(ValueError):
            parse_time('08:')
        with self.assertRaises(ValueError):
            parse_time('08:0')
        with self.assertRaises(ValueError):
            parse_time('23:60')
        with self.assertRaises(ValueError):
            parse_time('23-60')
        with self.assertRaises(ValueError):
            parse_time('08:00:0')
        with self.assertRaises(ValueError):
            parse_time('08:00:60')
        with self.assertRaises(ValueError):
            parse_time('08:00:59.')
        with self.assertRaises(ValueError):
            parse_time('08:00:59.9999')

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

    def test_invalid_aware_times(self):
        with self.assertRaises(ValueError):
            parse_time('08:30-3')
        with self.assertRaises(ValueError):
            parse_time('08:30-03:')
        with self.assertRaises(ValueError):
            parse_time('08:30-03:00:')
        with self.assertRaises(ValueError):
            parse_time('08:30-03:00:00')
        with self.assertRaises(ValueError):
            parse_time('08:30-24:00')
        with self.assertRaises(ValueError):
            parse_time('08:30+24:00')


class TimeZoneParserTestCase(TestCase):

    def test_valid_utc_timezone(self):
        self.assertEqual(parse_timezone('Z'), timedelta(0))
        self.assertEqual(parse_timezone('+00'), timedelta(0))
        self.assertEqual(parse_timezone('+00:00'), timedelta(0))
        self.assertEqual(parse_timezone('+0000'), timedelta(0))

    def test_invalid_utc_timezones(self):
        with self.assertRaises(ValueError):
            parse_timezone('z')
        with self.assertRaises(ValueError):
            parse_timezone('+0')
        with self.assertRaises(ValueError):
            parse_timezone('+000')
        with self.assertRaises(ValueError):
            parse_timezone('+00000')
        with self.assertRaises(ValueError):
            parse_timezone('-00')
        with self.assertRaises(ValueError):
            parse_timezone('-0000')

    def test_valid_timezones(self):
        self.assertEqual(parse_timezone('-03'), timedelta(hours=-3))
        self.assertEqual(parse_timezone('-03:00'), timedelta(hours=-3))
        self.assertEqual(parse_timezone('-03:35'), timedelta(hours=-3, minutes=-35))
        self.assertEqual(parse_timezone('-0300'), timedelta(hours=-3))
        self.assertEqual(parse_timezone('-23'), timedelta(hours=-23))
        self.assertEqual(parse_timezone('-23:59'), timedelta(hours=-23, minutes=-59))
        self.assertEqual(parse_timezone('-2359'), timedelta(hours=-23, minutes=-59))
        self.assertEqual(parse_timezone('+03'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+03:00'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+03:35'), timedelta(hours=3, minutes=35))
        self.assertEqual(parse_timezone('+0300'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+0300'), timedelta(hours=3))
        self.assertEqual(parse_timezone('+23'), timedelta(hours=23))
        self.assertEqual(parse_timezone('+23:59'), timedelta(hours=23, minutes=59))
        self.assertEqual(parse_timezone('+2359'), timedelta(hours=23, minutes=59))

    def test_invalid_timezones(self):
        with self.assertRaises(ValueError):
            parse_timezone('-3')
        with self.assertRaises(ValueError):
            parse_timezone('-03:')
        with self.assertRaises(ValueError):
            parse_timezone('-03:00:')
        with self.assertRaises(ValueError):
            parse_timezone('-03:00:00')
        with self.assertRaises(ValueError):
            parse_timezone('-24:00')
        with self.assertRaises(ValueError):
            parse_timezone('+24:00')
        with self.assertRaises(ValueError):
            parse_timezone('-25:00')
        with self.assertRaises(ValueError):
            parse_timezone('+25:00')

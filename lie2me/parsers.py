from datetime import time, timedelta, timezone
import re


def parse_time(string):
    pattern = ''.join([
        r'^([0-2][0-9])', # h
        r'(:([0-5][0-9]))?', # m
        r'(:([0-5][0-9]))?', # s
        r'(\.([0-9]{1,3}))?', # ms
        r'(Z|[+-][0-9:]+)?$', # tz
    ])
    match = re.match(pattern, string)
    if match is None:
        raise ValueError('Invalid time')
    h, _, m, _, s, _, ms, z = match.groups()
    h = int(h)
    m = int(m) if m is not None else 0
    s = int(s) if s is not None else 0
    ms = int(ms) * 1000 if ms is not None else 0
    tm = time(h, m, s, ms)
    if z is not None:
        tz = parse_timezone(z)
        tm = tm.replace(tzinfo=timezone(tz))
    return tm


def parse_timezone(string):
    pattern = r'^(Z)|([+-])([0-2][0-9])(:?([0-5][0-9]))?$'
    match = re.match(pattern, string)
    if match is None:
        raise ValueError('Invalid timezone')
    z, signal, h, _, m = match.groups()
    h = int(signal + h) if h is not None else 0
    m = int(signal + m) if m is not None else 0
    if h == 0 and signal == '-':
        raise ValueError('Invalid timezone')
    if abs((h * 60) + m) > (24 * 60) - 1:
        raise ValueError('Invalid timezone')
    return timedelta(hours=h, minutes=m)

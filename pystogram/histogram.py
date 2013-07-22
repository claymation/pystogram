import datetime

from .dateutil import timedelta_from_seconds, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND


class Histogram(object):
    def __init__(self, tree, resolution):
        self.tree = tree
        self.resolution = resolution
        self.interval = timedelta_from_seconds(resolution)

    @property
    def buckets(self):
        first_sample = datetime.datetime(*self.tree.least())
        last_sample = datetime.datetime(*self.tree.greatest())
        sample = first_sample
        while sample <= last_sample:
            bucket = Bucket(sample, self.resolution)
            node = self.tree.sum(bucket.key)
            yield bucket
            sample += self.interval


class Bucket(object):
    def __init__(self, start, resolution):
        self.start = start
        self.resolution = resolution
        self.value = 0
        self.format = '%Y'
        if resolution < YEAR:
            self.format += '-%m'
        if resolution < MONTH:
            self.format += '-%d'
        if resolution < DAY:
            self.format += ' %H'
        if resolution < HOUR:
            self.format += ':%M'
        if resolution < MINUTE:
            self.format += ':%S'

    def __str__(self):
        return '[%s] %s' % (self.timestamp, self.value)

    @property
    def timestamp(self):
        return self.start.strftime(self.format)

    # FIXME: What to call this?
    @property
    def key(self):
        key = [self.start.year]
        if self.resolution < YEAR:
            key.append(self.start.month)
        if self.resolution < MONTH:
            key.append(self.start.day)
        if self.resolution < DAY:
            key.append(self.start.hour)
        if self.resolution < HOUR:
            key.append(self.start.minute)
        if self.resolution < MINUTE:
            key.append(self.start.second)
        return key

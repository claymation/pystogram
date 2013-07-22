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
            node = self.tree.find(bucket.prefix)
            bucket.value = node.sum() if node is not None else 0
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

    @property
    def prefix(self):
        """
        Compute and return a key prefix for this bucket, based on its
        start timestamp and resolution.
        
        For example, a bucket with start timestamp 1969-07-20 20:18:00
        and resolution of 1 day yields a prefix of (1969, 7, 20).
        """
        prefix = [self.start.year]
        if self.resolution < YEAR:
            prefix.append(self.start.month)
        if self.resolution < MONTH:
            prefix.append(self.start.day)
        if self.resolution < DAY:
            prefix.append(self.start.hour)
        if self.resolution < HOUR:
            prefix.append(self.start.minute)
        if self.resolution < MINUTE:
            prefix.append(self.start.second)
        return prefix

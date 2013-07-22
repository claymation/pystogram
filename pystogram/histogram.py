import datetime

from pystogram.tree import Tree


SECOND = 1
MINUTE = SECOND * 60
HOUR   = MINUTE * 60
DAY    = HOUR * 24
MONTH  = DAY * 30
YEAR   = DAY * 365

# The multiplier applied when testing timestamp interval to guess a resolution.
# A value of 2.0 means the timestamp interval must be greater than 24 months in
# order to use a resolution of years
RESOLUTION_SCALE = 2.0


# FIXME: Where to put this?
def prefix(timestamp, resolution):
    """
    Compute and return a key prefix for this timestamp.
    """
    length = 1
    if resolution < YEAR: length += 1
    if resolution < MONTH: length += 1
    if resolution < DAY: length += 1
    if resolution < HOUR: length += 1
    if resolution < MINUTE: length += 1
    return timestamp.timetuple()[:length]


def guess_resolution(interval):
    """
    Compute a reasonable bucket resolution for the interval.
    """
    # FIXME: Improve?
    if interval > YEAR * RESOLUTION_SCALE:
        return YEAR
    elif interval > MONTH * RESOLUTION_SCALE:
        return MONTH
    elif interval > DAY * RESOLUTION_SCALE:
        return DAY
    elif interval > HOUR * RESOLUTION_SCALE:
        return HOUR
    elif interval > MINUTE * RESOLUTION_SCALE:
        return MINUTE
    else:
        return SECOND


# FIXME: Missing domain concepts: timestamp (essentially a datetime), key (essentially a time.struct_time tuple)

class Histogram(object):
    """
    An informal histogram useful for counting time-series data, dividing samples
    into equally-sized intervals (buckets), and computing aggregate counts of the
    samples within each bucket.
    """
    def __init__(self, Tree=Tree):
        """
        Construct a Histogram instance.

        Optional `Tree` parameter specifies the Tree-like class to use to count and aggregate samples.
        """
        self.tree = Tree()

    # FIXME: Rename this?
    def incr(self, timestamp):
        """
        Increment the count for this timestamp.
        """
        self.tree.incr(timestamp)

    def buckets(self, resolution=None):
        """
        Generate and yield buckets sized according to the passed or guessed resolution.
        """
        # FIXME: Subclass Tree into DateTimeTree so we don't have to do this conversion here?
        first_sample = datetime.datetime(*self.tree.least())
        last_sample = datetime.datetime(*self.tree.greatest())

        # Compute the bucket resolution
        sample_interval = (last_sample - first_sample).total_seconds()
        resolution = resolution if resolution is not None else guess_resolution(sample_interval)
        bucket_interval = datetime.timedelta(seconds=resolution)

        timestamp = first_sample
        while timestamp <= last_sample:
            node = self.tree.find(prefix(timestamp, resolution))
            bucket = Bucket(timestamp, node, resolution)
            yield bucket
            timestamp += bucket_interval


class Bucket(object):
    """
    Histogram bucket for a given time interval.
    """
    def __init__(self, start, node, resolution):
        self.start = start
        self.node = node

        # FIXME: Isn't this really a concern for the output formatter?
        self.resolution = resolution
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
        return '[%s] %s' % (self.timestamp, self.count)

    @property
    def count(self):
        """
        Return the count of samples in this bucket.
        """
        return self.node.sum()

    @property
    def timestamp(self):
        """
        Construct a string representation of this bucket's timestamp.
        """
        return self.start.strftime(self.format)

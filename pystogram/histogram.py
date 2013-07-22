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
    # FIXME: Improve?
    length = 1
    if resolution < YEAR: length += 1
    if resolution < MONTH: length += 1
    if resolution < DAY: length += 1
    if resolution < HOUR: length += 1
    if resolution < MINUTE: length += 1
    return timestamp.timetuple()[:length]


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

    def count(self, timestamp):
        """
        Increment the count for this timestamp.
        """
        self.tree.incr(timestamp)

    @property
    def first_sample(self):
        # FIXME: Subclass Tree into DateTimeTree so we don't have to do this conversion here?
        return datetime.datetime(*self.tree.least())

    @property
    def last_sample(self):
        # FIXME: Subclass Tree into DateTimeTree so we don't have to do this conversion here?
        return datetime.datetime(*self.tree.greatest())

    @property
    def sample_interval(self):
        return (self.last_sample - self.first_sample).total_seconds()

    @property
    def sample_resolution(self):
        """
        Compute a reasonable bucket resolution based on the sample interval.
        """
        # FIXME: Improve?
        interval = self.sample_interval
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
    
    def buckets(self, resolution=None):
        """
        Generate and yield buckets sized according to the passed or guessed resolution.
        """
        # Cache these properties locally
        first_sample = self.first_sample
        last_sample = self.last_sample

        # Compute the bucket resolution and interval (width)
        if resolution is None: resolution = self.sample_resolution
        bucket_interval = datetime.timedelta(seconds=resolution)

        timestamp = first_sample
        while timestamp <= last_sample:
            node = self.tree.find(prefix(timestamp, resolution))
            bucket = Bucket(timestamp, node)
            yield bucket
            timestamp += bucket_interval


# FIXME: If Bucket has no behaviour, only state, could we use a namedtuple instead?
class Bucket(object):
    """
    Histogram bucket for a given time interval.
    """
    # FIXME: This ought to take resolution and/or interval
    def __init__(self, start, node):
        self.start = start
        self.node = node
        self.count = node.sum()

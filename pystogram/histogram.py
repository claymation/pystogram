import datetime


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


class Histogram(object):
    def __init__(self, tree, resolution=None):
        self.tree = tree

        # Find the timestamp space boundaries and interval
        # FIXME: Subclass Tree into DateTimeTree so we don't have to do these conversions here?
        self.first_timestamp = datetime.datetime(*tree.least())
        self.last_timestamp = datetime.datetime(*tree.greatest())

        # Compute the bucket resolution
        self.resolution = resolution if resolution is not None else self.guess_resolution()
        self.bucket_interval = datetime.timedelta(seconds=self.resolution)

    def guess_resolution(self):
        """
        Compute a reasonable resolution given the timestamp interval.
        """
        seconds = (self.last_timestamp - self.first_timestamp).total_seconds()
        # FIXME: Improve?
        if seconds > YEAR * RESOLUTION_SCALE:
            return YEAR
        elif seconds > MONTH * RESOLUTION_SCALE:
            return MONTH
        elif seconds > DAY * RESOLUTION_SCALE:
            return DAY
        elif seconds > HOUR * RESOLUTION_SCALE:
            return HOUR
        elif seconds > MINUTE * RESOLUTION_SCALE:
            return MINUTE
        else:
            return SECOND

    @property
    def buckets(self):
        timestamp = self.first_timestamp
        while timestamp <= self.last_timestamp:
            node = self.tree.find(prefix(timestamp, self.resolution))
            value = node.sum() if node is not None else 0
            bucket = Bucket(timestamp, value, self.resolution)
            yield bucket
            timestamp += self.bucket_interval


class Bucket(object):
    def __init__(self, start, value, resolution):
        self.start = start
        self.value = value

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
        return '[%s] %s' % (self.timestamp, self.value)

    @property
    def timestamp(self):
        """
        Construct a string representation of this bucket's timestamp.
        """
        return self.start.strftime(self.format)

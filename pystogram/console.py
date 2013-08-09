import math
import shutil

# FIXME: Import these from elsewhere?
from .histogram import SECOND, MINUTE, HOUR, DAY, MONTH, YEAR


DEFAULT_CONSOLE_WIDTH = 80
PADDING = 2

# FIXME: embed timestamp format characters here
BUCKET_FORMAT = '{timestamp:{timestamp_length}s}  {bar:{bar_length}s}   {count:{count_length}d}'

# Chart bar ought not be narrower than 10 characters
MINIMUM_BAR_LENGTH = 10


def get_console_width():
    try:
        # Available in Python >= 3.3
        return shutil.get_terminal_size().columns
    except AttributeError:
        return DEFAULT_CONSOLE_WIDTH


class AsciiChart(object):
    """
    A text-based histogram chart drawn with ASCII characters.
    """
    def __init__(self, histogram):
        self.histogram = histogram

    def draw(self, width=None, resolution=None):
        """
        Draw the histogram at the desired resolution to stdout.
        """
        if width is None: width = get_console_width() - PADDING
        if resolution is None: resolution = self.histogram.sample_resolution

        # Construct bucket list
        buckets = list(self.histogram.buckets(resolution))
        if not buckets: return

        # Determine the bucket with the highest count
        max_count = max(map(lambda bucket: bucket.count, buckets))
        count_length = len(str(max_count))

        # Determine the timestamp format and length
        bucket = buckets[0]
        timestamp_format = self.get_timestamp_format(resolution)
        timestamp = bucket.start.strftime(timestamp_format)
        timestamp_length = len(timestamp)

        # Determine how much space we have left for bar
        # NB: Apparently, Python does not allow a length specifier to equal zero, so we pass
        #     bar_length=1 and then subtract 1 later on. Silly Python.
        output = BUCKET_FORMAT.format(timestamp=timestamp, timestamp_length=timestamp_length,
                                      bar='#', bar_length=1,
                                      count=max_count, count_length=count_length)
        output_length = len(output) - 1
        bar_length = width - output_length

        if bar_length < MINIMUM_BAR_LENGTH:
            raise Exception("Chart cannot be drawn in the available width.")

        for bucket in buckets:
            timestamp = bucket.start.strftime(timestamp_format)
            bar = '*' * int(math.ceil(float(bar_length * bucket.count) / max_count))
            print(BUCKET_FORMAT.format(timestamp=timestamp, timestamp_length=timestamp_length,
                                       bar=bar, bar_length=bar_length,
                                       count=bucket.count, count_length=count_length))

    def get_timestamp_format(self, resolution):
        """
        Construct a strftime format string for timestamps, using
        the resolution to determine how much detail to include.
        """
        format = '%Y'
        if resolution < YEAR:
            format += '-%m'
        if resolution < MONTH:
            format += '-%d'
        if resolution < DAY:
            format += ' %H'
        if resolution < HOUR:
            format += ':%M'
        if resolution < MINUTE:
            format += ':%S'

        return format

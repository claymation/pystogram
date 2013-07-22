import collections


class Tree(collections.defaultdict):
    """
    A purpose-built prefix tree for counting and aggregating timestamps.

        >>> tree = Tree()

    Keys are tuples of integers, compatible with `time.struct_time` objects.

    You can increment a key:
    
        >>> tree.incr((1969, 3, 3))
        1
        >>> tree.incr((1969, 5, 18), 2)
        2

     or set its value directly:

        >>> tree.set((1969, 7, 16), 3)
        3
    
    You can get a key's value:
    
        >>> tree.get((2013, 3, 3))
        1
    
    or the sum of its value plus all of its descendants' values:
    
        >>> tree.sum((1969,))
        6

    At this point, the tree looks like:

                                    tree root
                                        |
                                        |
                            node(key=1969, value=0)
                                        |
                                        |
                +-----------------------+-----------------------+
                |                       |                       |
                |                       |                       |
      node(key=3, value=0)    node(key=5, value=0)    node(key=7, value=0)
                |                       |                       |
                |                       |                       |
      node(key=3, value=1)   node(key=18, value=1)   node(key=16, value=1)

    Each node is, in fact, a new Tree instance.

    Two utility methods return the least and greatest keys in the tree:
    
        >>> tree.least()
        (1969, 3, 3)
        >>> tree.greatest()
        (1969, 7, 16)
    """

    def __init__(self):
        super(Tree, self).__init__(Tree)
        self.value = 0

    def get(self, key):
        """
        Get the value for the supplied key.
        
        Returns None if the key is not found.
        """
        node = self._find(key)
        if node is not None:
            return node.value

    def set(self, key, value):
        """
        Set the value for the supplied key.
        """
        node = self._insert(key)
        node.value = value
        return node.value

    def incr(self, key, increment=1):
        """
        Increment the key's value by the supplied increment value.
        
        If the key does not exist, it is created and its value
        initialized to 0 before being incremented.

        To decrement a key's value, pass a negative increment.
        """
        node = self._insert(key)
        node.value += increment
        return node.value

    def sum(self, key):
        """
        Return the sum of the key's value, plus all of the key's
        descendants' values.
        """
        total = self.value
        for node in self.values():
            total += node.sum(key[1:])
        return total

    def least(self):
        """
        Find and return the least key in the tree.
        """
        return self._walk(0)

    def greatest(self):
        """
        Find and return the greatest key in the tree.
        """
        return self._walk(-1)

    def _find(self, key):
        """
        Find and return the node given by the supplied key.
        
        Returns None if the key is not found.
        """
        if not key:
            return self

        # `defaultdict.get()` does not create new instances for unknown keys
        node = self.get(key[0])

        if node is not None:
            return node._find(key[1:])

    def _insert(self, key):
        """
        Find and return the node given by the supplied key,
        creating it if it doesn't already exist.
        """
        if not key:
            return self

        # `defaultdict.__getitem__()` creates new instances for unknown keys
        node = self[key[0]]

        return node._insert(key[1:])

    def _walk(self, index):
        """
        Construct a key by walking the tree, always branching the same way
        as determined by the supplied index.

        The only practical values for `index` are:
        
             0, which follows the left-most (least key) branch
            -1, which follows the right-most (greatest key) branch
        """
        # Have we reached a leaf node?
        if len(self) == 0:
            return []

        key = self.sorted_keys[index]
        node = self[key]
        return [key] + node._walk(index)

    @property
    def sorted_keys(self):
        """
        Return a sorted list of this node's keys.
        """
        return sorted(self.keys())

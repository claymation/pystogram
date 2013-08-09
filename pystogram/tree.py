import collections


class PrefixTree(collections.defaultdict):
    """
    A generic prefix tree (or trie) for counting and aggregating composite keys.

        >>> tree = PrefixTree()

    Keys are iterables of comparable, hashable objects, such as strings or tuples of integers.

    Basic operations include incrementing a key:
    
        >>> tree.incr('monty')
        1

     set a key's value directly:

        >>> tree.set('monty', 42)
        42
    
    and getting a key's value:
    
        >>> tree.get('monty')
        42
    
    But the power of the prefix tree comes from being able to aggregate by key prefix. To demonstrate,
    let's add some more keys to the tree:

        >>> tree.incr('python')
        1
        >>> tree.incr('pylon')
        1
        >>> tree.incr('panda')
        1
    
    At this point, the tree looks like:

                                        tree root
                                            |
                +---------------------------+-------------------+
                |                                               |
    node(key='m', value=0)                          node(key='p', value=0)
                |                                               |
    node(key='o', value=0)              +-----------------------+---------------+
                |                       |                                       |
    node(key='n', value=0)    node(key='a', value=0)                node(key='y', value=0)
                |                       |                                       |
    node(key='t', value=0)    node(key='n', value=0)            +---------------+-------------+
                |                       |                       |                             |
    node(key='y', value=42)   node(key='d', value=0)    node(key='l', value=0)    node(key='t', value=0)
                                        |                       |                             |
                              node(key='a', value=1)    node(key='o', value=0)    node(key='h', value=0)
                                                                |                             |
                                                        node(key='n', value=1)    node(key='o', value=0)
                                                                                              |
                                                                                  node(key='n', value=1)

    Each node is actually a new PrefixTree instance.

    Now we can ask interesting questions like, "what's the frequency of keys starting with 'py'?":

        >>> tree.find('py').sum()
        2

    Two utility methods return the node for the specified key:
    
        >>> tree.find('grail') is None    # will not create the node if it does not exist
        True

        >>> tree.insert('grail') is None  # will create the node with an initial value of 0
        False

    Two utility methods return the least and greatest keys in the tree:
    
        >>> tree.least()
        ['g', 'r', 'a', 'i', 'l']

        >>> tree.greatest()
        ['p', 'y', 't', 'h', 'o', 'n']

    Note that keys are represented as tuples internally, so if your keys are strings, you'll
    probably want to join the individual key characters back into a string:

        >>> ''.join(tree.least())
        'grail'

    """

    def __init__(self):
        super(PrefixTree, self).__init__(PrefixTree)
        self.value = 0

    def get(self, key):
        """
        Get the value for the supplied key.
        
        Returns None if the key is not found.
        """
        node = self.find(key)
        if node is not None:
            return node.value

    def set(self, key, value):
        """
        Set the value for the supplied key.
        """
        node = self.insert(key)
        node.value = value
        return node.value

    def incr(self, key, increment=1):
        """
        Increment the key's value by the supplied increment value.
        
        If the key does not exist, it is created and its value
        initialized to 0 before being incremented.

        To decrement a key's value, pass a negative increment.
        """
        node = self.insert(key)
        node.value += increment
        return node.value

    # FIXME: Probably need a better name for this ... aggregate()?
    def sum(self):
        """
        Return the sum of this node's value plus all of the node's
        descendants' values.
        """
        total = self.value
        for child in self.values():
            total += child.sum()
        return total

    # FIXME: Could we use min() instead?
    def least(self):
        """
        Find and return the least key in the tree.
        """
        return self.walk(0)

    # FIXME: Could we use max() instead?
    def greatest(self):
        """
        Find and return the greatest key in the tree.
        """
        return self.walk(-1)

    def find(self, key):
        """
        Find and return the node given by the supplied key.
        
        Returns None if the key is not found.
        """
        if not key:
            return self

        # `defaultdict.get()` does not create new instances for unknown keys
        node = super(PrefixTree, self).get(key[0])

        if node is not None:
            return node.find(key[1:])

    def insert(self, key):
        """
        Find and return the node given by the supplied key,
        creating it if it doesn't already exist.
        """
        if not key:
            return self

        # `defaultdict.__getitem__()` creates new instances for unknown keys
        node = self[key[0]]

        return node.insert(key[1:])

    def walk(self, index):
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
        return [key] + node.walk(index)

    
    @property
    def sorted_keys(self):
        """
        Return a sorted list of this node's keys.
        """
        return sorted(self.keys())

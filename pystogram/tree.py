import collections


class Tree(collections.defaultdict):
    """
    A simple prefix tree (trie) built on top of defaultdict.
    """
    def __init__(self, value=0):
        super(Tree, self).__init__(Tree)
        self.value = value

    # FIXME: Is traverse the right method? Should it take an index? Should we have a least()/greatest() or left()/right()?
    def traverse(self, index):
        if len(self) == 0:
            return []
        keys = sorted(self.keys())
        key = keys[index]
        nodes = self[key].traverse(index)
        nodes.insert(0, key)
        return nodes

    def find(self, keys):
        if not keys:
            return self
        key = keys.pop(0)
        return self[key].find(keys)

    def sum(self):
        count = self.value
        for key in self.keys():
            count += self[key].sum()
        return count

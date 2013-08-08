from pystogram.tree import PrefixTree


def test_empty_tree_has_zero_sum():
    tree = PrefixTree()
    assert 0 == tree.sum()

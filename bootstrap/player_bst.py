"""Bootstrap subproject: a BST that stores players by a stat.

Built on the BSTree class from HW08. Two things are new:
  1. A node keeps a LIST of players, so players with the same stat are kept.
  2. range_query(lo, hi) returns every player whose stat is between lo and hi.
"""


class Node:
    def __init__(self, key, value):
        self.key = key          # the stat we sort by, e.g. 25.3 points per game
        self.values = [value]   # every player who has exactly that stat
        self.left = None        # subtree with smaller keys
        self.right = None       # subtree with bigger keys


class PlayerBST:
    def __init__(self):
        self.root = None        # an empty tree has no root node
        self.size = 0           # how many players (not nodes) are stored

    # Support for len(tree)
    def __len__(self):
        return self.size

    # Add one player under the given stat
    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
        self.size += 1

    def _insert(self, root, key, value):
        # Empty spot: this is where the new node goes.
        if root is None:
            return Node(key, value)

        # Same stat as this node: add the player to its list.
        # (The HW08 version ignored duplicates here.)
        if key == root.key:
            root.values.append(value)
            return root

        # Otherwise go left for smaller keys, right for bigger keys.
        if key < root.key:
            root.left = self._insert(root.left, key, value)
        else:
            root.right = self._insert(root.right, key, value)
        return root

    # Height of the tree (-1 when empty), same as HW08
    def height(self):
        return self._height(self.root)

    def _height(self, root):
        if root is None:
            return -1
        return 1 + max(self._height(root.left), self._height(root.right))

    # Return every player with lo <= stat <= hi, in increasing stat order
    def range_query(self, lo, hi):
        result = []
        self._range_query(self.root, lo, hi, result)
        return result

    def _range_query(self, root, lo, hi, result):
        if root is None:
            return

        # Everything on the left is smaller than root.key.
        # Only worth visiting if something smaller could still be >= lo.
        if lo < root.key:
            self._range_query(root.left, lo, hi, result)

        # This node itself is inside the range: take its players.
        if lo <= root.key <= hi:
            result.extend(root.values)

        # Everything on the right is bigger than root.key.
        # Only worth visiting if something bigger could still be <= hi.
        if root.key < hi:
            self._range_query(root.right, lo, hi, result)

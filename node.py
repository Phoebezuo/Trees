"""
Tree Node
----------

This node represents an item in the tree. Each node contains its key as well as
the value of the subtree rooted at this node. It supports operations to add
children, as well as check if this is a leaf or not.

The subtree value is the aggregate value of the keys in the subtree rooted at this node.
If the keys in the subtree are k_1, k_2, ..., k_n the subtree value
should be fn(k_1, fn(k_2, ... fn(k_{n-1}, k_n))) where fn is
the Tree's aggregating function.
Assume fn is associative and commutative, i.e., any order of the keys yields
in the above formula yields the same result.
If this node has no children, then subtree_value = self.key.
"""


class Node:
    """
    Node Class
    - Init: Sets the basic information such as the key, children, and value of
    subtree.
    - is_external(): Checks if the node is a leaf.
    - children(): returns the list of children.
    """

    def __init__(self, key, parent=None):
        """
        The initialisation of the node sets the key and instantiates the
        children (as empty).
        :param key: The value of the node.
        :param parent: The parent of the node.
        """
        self.key = key
        self.parent = parent
        self.subtree_value = key
        self.children = []


    def is_external(self):
        """
        Checks if the node is a leaf node in the tree.
        :return: Boolean, True if leaf, False otherwise.
        """

        return len(self.children) == 0

    def get_children(self):
        """
        Returns the children of the current node.
        :return: List of children.
        """

        # Can also access this using "node.children", but putting
        # this here for ease of use and standard usage things
        # for other languages people might be used to.
        return self.children

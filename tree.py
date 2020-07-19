import node

class Tree:
    def __init__(self, fn):
        self.fn = fn
        self.root = None

    def create_root(self, root_key):
        assert self.root == None, "cannot create root in non-empty tree"
        self.root = self.new_node(root_key)

    def new_node(self, key):
        return node.Node(key)

    def put(self, parent, child):
        parent.children.append(child) # add child to the list of children
        child.parent = parent #  connect child to parent

        self.update_subtree(parent)

    def flatten(self, node, fn):
        if node.is_external():
            return node;

        # operate on each children
        result = node.key

        # find the last child
        for c in node.children:
            cursor = c
            result = fn(result, cursor.key)

            while not cursor.is_external():
                for c in cursor.children:
                    cursor = c
                    result = fn(result, cursor.key)

        # update node key
        node.key = result
        node.subtree_value = result
        node.children = []

        if node.parent != None:
            self.update_subtree(node.parent)

        return node;

    def swap(self, node_a, node_b):
        if node_a == node_b:
            return;

        # update subtree_value from swapping item onwards to its key
        cursor1 = node_a
        while cursor1.parent != None:
            cursor1.subtree_value = cursor1.key
            cursor1 = cursor1.parent

        cursor2 = node_b
        while cursor2.parent != None:
            cursor2.subtree_value = cursor2.key
            cursor2 = cursor2.parent

        a_parent = node_a.parent
        b_parent = node_b.parent

        # clear connect between swapping item and their parents
        node_a.parent = None;
        node_b.parent = None;
        a_parent.children.remove(node_a)
        b_parent.children.remove(node_b)

        # connect swapping item connect to tree
        self.put(b_parent, node_a)
        self.put(a_parent, node_b)

        self.update_subtree(node_a)
        self.update_subtree(node_b)

    def update_subtree(self, node):
        node.subtree_value = node.key

        for child in node.children:
            node.subtree_value = self.fn(node.subtree_value, child.subtree_value)

        if node.parent != None:
            self.update_subtree(node.parent)

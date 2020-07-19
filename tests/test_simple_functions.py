import unittest
import node
import tree
import operator

def assert_equal(got, expected, msg):
    """
    Simple asset helper
    """
    assert expected == got, \
        "[{}] Expected: {}, got: {}".format(msg, expected, got)

class SimpleFunctionsTestCase(unittest.TestCase):

    def setUp(self):
        self.max_agg = lambda x, y: x if x > y else y
        self.tree = tree.Tree(self.max_agg)
        self.tree.create_root(5)

        self.tree2 = tree.Tree(self.max_agg)
        self.tree2.create_root(1)

        self.xor_tree = tree.Tree(operator.xor)
        self.xor_tree.create_root(1)

    def test_can_insert_single(self):
        """
        Inserts a single node into the tree.

        r
        |
        A(10)

        #score(1)
        """

        new_node = self.tree.new_node(10)
        self.tree.put(self.tree.root, new_node)

        # Check
        assert_equal(len(self.tree.root.children), 1, "root children")
        assert_equal(self.tree.root.subtree_value, 10, "root subtree value")

    def test_can_insert_two(self):
        """
        Makes a simple tree.
            r
          /   \
        A(10)  B(8)

        #score(1)
        """
        node_a = self.tree.new_node(10)
        node_b = self.tree.new_node(8)

        self.tree.put(self.tree.root, node_a)

        # Check
        assert_equal(len(self.tree.root.children), 1, "root children")
        assert_equal(self.tree.root.subtree_value, 10, "root subtree value")

        self.tree.put(self.tree.root, node_b)

        # check
        assert_equal(len(self.tree.root.children), 2, "root children")
        assert_equal(self.tree.root.subtree_value, 10, "root subtree value")

    def test_xor_tree(self):
        """
        Makes a simple tree.
            r
          /   \
        A(0)  B(1)

        #score(1)
        """
        node_a = self.xor_tree.new_node(0)
        node_b = self.xor_tree.new_node(1)

        self.xor_tree.put(self.xor_tree.root, node_a)

        # Check
        assert_equal(len(self.xor_tree.root.children), 1, "root children")
        assert_equal(self.xor_tree.root.subtree_value, 1, "root subtree value")
        assert_equal(node_a.subtree_value, 0, "node a subtree value")

        self.xor_tree.put(self.xor_tree.root, node_b)

        # check
        assert_equal(len(self.xor_tree.root.children), 2, "root children")
        assert_equal(node_b.subtree_value, 1, "node b subtree value")
        assert_equal(self.xor_tree.root.subtree_value, 0, "root subtree value")

    def test_flatten_external(self):
        """
        Flatten should merge

            r             r
          /   \    >    /  \
        A(4) B(5)    A(4)  B(5)
            / |            / |
        C(6) D(59)     C(6) D(59)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(6)
        node_d = self.tree.new_node(59)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)

        self.tree.flatten(node_c, operator.add)

        assert_equal(len(node_b.children), 2, "node b children")
        assert node_c.is_external(), "Node should be leaf after flattening."

        assert_equal(node_b.subtree_value, 59, "node b subtree_value")
        assert_equal(root.subtree_value, 59, "root subtree_value")


    def test_flatten_with_root_one(self):
        """
        Flatten should merge

           r(1)          r(1)
          /   \    >    /  \
        A(4) B(5)    A(4)  newB(0)
            / |
        C(6) D(0)

        #score(2)
        """

        root = self.tree2.root
        node_a = self.tree2.new_node(4)
        node_b = self.tree2.new_node(5)
        node_c = self.tree2.new_node(6)
        node_d = self.tree2.new_node(0)

        self.tree2.put(root, node_a)
        self.tree2.put(root, node_b)
        self.tree2.put(node_b, node_c)
        self.tree2.put(node_b, node_d)

        assert_equal(len(node_b.children), 2, "node b children")

        self.tree2.flatten(node_b, operator.mul)

        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        assert_equal(node_b.subtree_value, 0, "node b subtree_value")
        assert_equal(root.subtree_value, 4, "root subtree_value")
        assert_equal(root.key, 1, "root key")

    def test_bubble_up_value(self):
        """
        Addition of third level, should bubble up the values

           root
          /    \
        A(4)   B(5)
        |
        C(6)
        |
        D(8)

        #score(2)
        """
        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(6)
        node_d = self.tree.new_node(8)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)

        assert_equal(len(self.tree.root.children), 2, "root children")
        assert_equal(self.tree.root.subtree_value, 5, "root subtree value")

        self.tree.put(node_a, node_c)

        assert_equal(self.tree.root.subtree_value, 6, "root subtree value")
        assert_equal(node_a.subtree_value, 6, "node a subtrtee value")

        self.tree.put(node_a, node_c)
        self.tree.put(node_c, node_d)

        assert_equal(self.tree.root.subtree_value, 8, "root subtree value")
        assert_equal(node_a.subtree_value, 8, "node a subtree value")

    def test_simple_flatten_merge(self):
        """
        Flatten should merge

            r             r
          /   \    >    /  \
        A(4) B(5)    A(4)  B_NEW(70)
            / |
        C(6) D(59)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(6)
        node_d = self.tree.new_node(59)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)

        self.tree.flatten(node_b, operator.add)

        # It should be a leaf.
        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        # The node key should be the sum of the children.
        assert_equal(node_b.key, 70, "node b key")

    def test_simple_flatten_merge_mult_line(self):
        """
        Flatten should merge

              r             r
            /   \    >    /  \
          A(4) B(5)    A(4)  B_NEW(73)
              / |
          C(6) D(59)
                |
               E(3)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(6)
        node_d = self.tree.new_node(59)
        node_e = self.tree.new_node(3)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)
        self.tree.put(node_b, node_e)

        self.tree.flatten(node_b, operator.add)

        # It should be a leaf.
        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        # The node key should be the sum of the children.
        assert_equal(node_b.key, 73, "node b key")
        assert_equal(node_b.subtree_value, 73, "node b subtree key")

    def test_flatten_merge_with_mul(self):
        """
        Flatten should merge

              r             r
            /   \    >    /  \
          A(4) B(5)    A(4)  B_NEW(180)
              / |
          C(2) D(3)
                |
               E(6)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(2)
        node_d = self.tree.new_node(3)
        node_e = self.tree.new_node(6)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)
        self.tree.put(node_b, node_e)

        assert_equal(node_b.subtree_value, 6, "node b subtree value")
        assert_equal(root.subtree_value, 6, "root subtree value")

        self.tree.flatten(node_b, operator.mul)

        # It should be a leaf.
        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        # The node key should be the sum of the children.
        assert_equal(node_b.key, 180, "node b key")
        assert_equal(node_b.subtree_value, 180, "node b subtree value")
        assert_equal(root.subtree_value, 180, "root subtree value") # my 6

    def test_flatten_merge_with_max(self):
        """
        Flatten should merge

              r             r
            /   \    >    /  \
          A(4) B(5)    A(4)  B_NEW(6)
              / |
          C(2) D(3)
                |
               E(6)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(2)
        node_d = self.tree.new_node(3)
        node_e = self.tree.new_node(6)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)
        self.tree.put(node_b, node_e)

        self.tree.flatten(node_b, self.max_agg)

        # It should be a leaf.
        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        # The node key should be the sum of the children.
        assert_equal(node_b.key, 6, "node b key")
        assert_equal(node_b.subtree_value, 6, "node b subtree value")

    def test_flatten_merge_with_mul_with_zero(self):
        """
        Flatten should merge

              r             r
            /   \    >    /  \
          A(4) B(5)    A(4)  B_NEW(0)
              / |
          C(2) D(3)
                |
               E(0)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(2)
        node_d = self.tree.new_node(3)
        node_e = self.tree.new_node(0)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)
        self.tree.put(node_b, node_e)

        assert_equal(node_b.subtree_value, 5, "node b subtree value")
        assert_equal(root.subtree_value, 5, "root subtree value")

        self.tree.flatten(node_b, operator.mul)

        # It should be a leaf.
        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        # The node key should be the sum of the children.
        assert_equal(node_b.key, 0, "node b key")
        assert_equal(node_b.subtree_value, 0, "node b subtree value")
        assert_equal(root.subtree_value, 5, "root subtree value")
        assert_equal(len(root.children), 2, "root children")
        assert_equal(root.children[1].key, 0, "roob b key")

    def test_flatten_merge_at_zero(self):
        """
        Flatten should merge

              r             r
            /   \    >    /  \
          A(4) B(5)    A(4)  B_NEW(6)
              / |
          C(2) D(0)
                |
               E(6)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(2)
        node_d = self.tree.new_node(0)
        node_e = self.tree.new_node(6)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)
        self.tree.put(node_b, node_e)

        self.tree.flatten(node_b, self.max_agg)

        # It should be a leaf.
        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        # The node key should be the sum of the children.
        assert_equal(node_b.key, 6, "node b key")
        assert_equal(node_b.subtree_value, 6, "node b subtree value")

    def test_flatten_merge_at_root(self):
        """
        Flatten should merge

             r(5)
            /   \    >    r(5040)
          A(4) B(1)
              / |
          C(2) D(3)
                |
               E(6)
                |
               F(7)

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(1)
        node_c = self.tree.new_node(2)
        node_d = self.tree.new_node(3)
        node_e = self.tree.new_node(6)
        node_f = self.tree.new_node(7)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)
        self.tree.put(node_d, node_e)
        self.tree.put(node_e, node_f)

        assert_equal(len(root.children), 2, "root's children")

        self.tree.flatten(root, operator.mul)

        # It should be a leaf.
        assert_equal(len(root.children), 0, "root's children")
        assert root.is_external(), "the tree has only a single root"

        # The node key should be the sum of the children.
        assert_equal(root.key, 5040, "root key")
        assert_equal(root.subtree_value, 5040, "root subtree_value")

    def test_example_swap(self):
        """
        Can perform swap as shown in example

           A(5)
           / \
         C(2) D(8)
          |
         B(10)

         > tree.swap(B, D)

           A(5)
           / \
         C(2) B(10)
          |
         D(8)

        #score(2)
        """

        root = self.tree.root
        C = self.tree.new_node(2)
        B = self.tree.new_node(10)
        D = self.tree.new_node(8)

        self.tree.put(root, C)
        self.tree.put(root, D)
        self.tree.put(C, B)

        assert_equal(C.subtree_value, 10, "node c subtree value")
        assert_equal(root.subtree_value, 10, "root subtree value")

        self.tree.swap(B, D)

        assert_equal(C.subtree_value, 8, "node c subtree value")
        assert_equal(root.subtree_value, 10, "root subtree value")

    def test_swap_with_itself(self):
        """
        Can perform swap as shown in example

           A(5)
           / \
         C(2) D(8)
          |
         B(10)

         > tree.swap(B, B)

            A(5)
            / \
          C(2) D(8)
           |
          B(10)

        #score(2)
        """

        root = self.tree.root
        C = self.tree.new_node(2)
        B = self.tree.new_node(10)
        D = self.tree.new_node(8)

        self.tree.put(root, C)
        self.tree.put(root, D)
        self.tree.put(C, B)

        assert_equal(C.subtree_value, 10, "node c subtree value")
        assert_equal(root.subtree_value, 10, "root subtree value")

        self.tree.swap(B, B)

        assert_equal(C.subtree_value, 10, "node c subtree value")
        assert_equal(root.subtree_value, 10, "root subtree value")
        assert_equal(root.key, 5, "root key")

    def test_simple_swap(self):
        """
        Swap subtree A and B correctly.

                r(5)
            /    |    \
          C(6)  B(5)  A(4)
        /  |          /  \
    G(10) H(11)     D(7)  E(8)
                           |
                          F(9)

        """

        # Generate the nodes
        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(6)
        node_d = self.tree.new_node(7)
        node_e = self.tree.new_node(8)
        node_f = self.tree.new_node(9)
        node_g = self.tree.new_node(10)
        node_h = self.tree.new_node(11)

        # Put them into the tree.
        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(root, node_c)
        self.tree.put(node_a, node_d)
        self.tree.put(node_a, node_e)
        self.tree.put(node_e, node_f)
        self.tree.put(node_c, node_g)
        self.tree.put(node_c, node_h)

        assert_equal(len(root.children), 3, "number of children at root")

        # Check that the values are correct
        assert_equal(root.subtree_value, 11, "root subtree value")
        assert_equal(node_c.subtree_value, 11, "node c subtree value")
        assert_equal(node_a.subtree_value, 9, "node a subtree value")

        # Let's get swapping!
        self.tree.swap(node_a, node_c)

        """
        Swap a and c.

                r(5)
            /    |    \
          A(4)  B(5)  C(6)
        /  |          /  \
     D(7) E(8)     G(10)  H(11)
           |
          F(9)

        """
        assert_equal(len(root.children), 3, "number of children at root")
        assert_equal(root.subtree_value, 11, "root subtree value")
        assert_equal(node_c.subtree_value, 11, "node c subtree value")
        assert_equal(node_c.key, 6, "node c key")
        assert_equal(node_a.subtree_value, 9, "node a subtree value")

        assert node_c.parent == root, "node c should be root's child"
        assert node_a.parent == root, "node a should be root's child"

        assert_equal(len(node_c.children), 2, "node c children")
        assert_equal(len(node_a.children), 2, "node a children")


        assert_equal(len(root.children), 3, "number of children at root")

        # ¯\_(ツ)_/¯
        self.tree.swap(node_f, node_c)

        """
        Swap f and c.

                r(5)
            /    |    \
          A(4)  B(5)  F(9)
        /  |
     D(7) E(8)
           |
          C(6)
          /  \
      G(10)  H(11)

        """

        # Root value should stay
        assert_equal(self.tree.root.subtree_value, 11, "root subtree value")

        # Parent and children should have swapped correctly
        assert node_f.parent == root, "Node should swap parent."
        assert node_c.parent == node_e, "Node should swap parent."
        assert node_c in node_e.children, "Node should add children."

        assert_equal(node_f.subtree_value, 9, "node f subtree value")
        assert_equal(node_a.subtree_value, 11, "node a subtree value")
        assert_equal(node_e.subtree_value, 11, "node e subtree value")
        assert_equal(node_c.subtree_value, 11, "node c subtree value")
        assert_equal(node_d.subtree_value, 7, "node d subtree value")
        assert_equal(len(node_a.children), 2, "node a children")

        assert_equal(len(root.children), 3, "number of children at root")

        self.tree.flatten(node_e, operator.mul)

        """
        Swap f and c.

                r(5)
            /    |    \
          A(4)  B(5)  F(9)
        /   \
     D(7)  newE(5280)

        """

        assert_equal(node_e.subtree_value, 5280, "node e subtree_value")
        assert_equal(node_a.subtree_value, 5280, "node a subtree_value")
        assert_equal(node_e.key, 5280, "node e key")
        assert_equal(len(root.children), 3, "number of children at root")
        assert_equal(root.subtree_value, 5280, "root subtree_value")


if __name__ == '__main__':
    unittest.main()

#------------------------------------------------------------------------------
#  Copyright (c) 2009 Richard W. Lincoln
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
#------------------------------------------------------------------------------

""" Defines tests for Godot graphs and sub-elements.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import unittest

from godot.api \
    import Graph, Subgraph, Cluster, Node, Edge

#------------------------------------------------------------------------------
#  "NodeTestCase" class:
#------------------------------------------------------------------------------

class NodeTestCase(unittest.TestCase):
    """ Defines a test case for nodes.
    """

    def test_create_node(self):
        """ Test creation of a node.
        """
        node = Node(ID="test_node", shape="circle")
        self.failUnless(node.name == "test_node")
        self.assertEqual(node.shape, "circle")

#------------------------------------------------------------------------------
#  "EdgeTestCase" class:
#------------------------------------------------------------------------------

class EdgeTestCase(unittest.TestCase):
    """ Defines a test case for edges.
    """

    def test_create_edge(self):
        """ Test creation of a edge.
        """
        edge = Edge("a", Node("b"), dir="both", label="Test Edge")
        self.failUnless(edge.tail_node.name == "a")
        self.failUnless(edge.head_node.name == "b")
        self.assertEqual(edge.dir, "both")
        self.assertEqual(edge.label, "Test Edge")

#------------------------------------------------------------------------------
#  "SubgraphTestCase" class:
#------------------------------------------------------------------------------

class SubgraphTestCase(unittest.TestCase):
    """ Defines a test case for subgraphs.
    """

    def test_create_subgraph(self):
        """ Test creation of a subgraph.
        """
        subgraph = Subgraph(ID="subgraph1", rank="max")
        self.failUnless(subgraph.name == "subgraph1")
        self.assertEqual(subgraph.rank, "max")


    def test_create_cluster(self):
        """ Test creation of a cluster.
        """
        cluster = Cluster(ID="cluster_1", fixedsize=True)
        self.failUnless(cluster.name == "cluster_1")
        self.assertTrue(cluster.fixedsize)


    def test_cluster_name(self):
        """ Test that a cluster's name always starts 'cluster'.
        """
        cluster = Cluster(ID="small")
        self.failUnless(cluster.name == "cluster_small")

#------------------------------------------------------------------------------
#  "GraphTestCase" class:
#------------------------------------------------------------------------------

class GraphTestCase(unittest.TestCase):
    """ Defines a test case for Godot graph objects.
    """

    def test_create(self):
        """ Test creation of a graph.
        """
        g = Graph(name="graph", strict=True, directed=False)
        self.failUnless(g.name == "graph")
        self.assertTrue(g.strict)
        self.assertFalse(g.directed)


    def test_create_with_attributes(self):
        """ Test creation of a graph with attributes.
        """
        g = Graph(mode="KK", label="testgraph")
        self.assertEqual(g.mode, "KK")
        self.assertEqual(g.label, "testgraph")


    def test_add_node(self):
        """ Test adding nodes to a graph.
        """
        g = Graph()
        g.nodes.append( Node(ID="node1") )
        g.add_node("node2")
        g.add_node( Node("node3") )
        self.assertEqual(len(g), 3)


    def test_add_equal_nodes(self):
        """ Test adding nodes with existing names.
        """
        g = Graph()
        g.add_node("a", label="test1")
        g.add_node("a", fixedsize=True)
        g.add_node("a", label="test2", shape="circle")
        self.assertEqual(len(g), 1)

        n = g.get_node("a")
        self.assertTrue(n.fixedsize)
        self.assertEqual(n.label, "test2")
        self.assertEqual(n.shape, "circle")


    def test_add_nonstring_nodes(self):
        """ Test adding nodes with non-string names.
        """
        g = Graph()
        n = g.add_node(6)
        self.assertEqual(n.ID, "6")
        n = g.add_node(3.14)
        self.assertEqual(n.ID, "3.14")
        self.assertEqual(len(g), 2)


    def test_add_edge(self):
        """ Test adding edges to a graph.
        """
        g = Graph()
        n1, n2, n3 = Node("N1"), Node("N2"), Node("N3")
        g.edges.append( Edge(n1, n2) )
        g.add_edge("tail", "head", label="edge1")
        g.add_edge(n2, n3, color="blue")

        self.assertEqual(len(g.edges), 3)
        self.assertEqual(g.edges[1].label, "edge1")


    def test_add_subgraph(self):
        """ Test adding subgraphs to a graph.
        """
        g = Graph()
        subgraph = Subgraph(ID="sub1", level=1)
        g.add_subgraph(subgraph)
        g.add_subgraph("sub2")
        self.assertEqual(len(g.subgraphs), 2)


    def test_add_cluster(self):
        """ Test adding clusters to a graph.
        """
        g = Graph()
        cluster = Cluster(ID="cluster0", level=1)
        g.add_cluster(cluster)
        g.add_cluster("cluster1")
        self.assertEqual(len(g.clusters), 2)


if __name__ == "__main__":
    unittest.main()

# EOF -------------------------------------------------------------------------

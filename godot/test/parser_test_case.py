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

""" Defines tests for the Dot data parser.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import unittest

from os.path import join, dirname

from godot.api import Graph, Subgraph, Cluster, Node, Edge
from godot.dot_data_parser import GodotDataParser

CLUSTER_GRAPH = join(dirname(__file__), "data", "clust.dot")
COLORS_GRAPH = join(dirname(__file__), "data", "colors.dot")

#------------------------------------------------------------------------------
#  "ParserTestCase" class:
#------------------------------------------------------------------------------

class ParserTestCase(unittest.TestCase):
    """ Defines a test case for the Dot data parser.
    """

    def test_parse_cluster(self):
        """ Test parsing of a graph with clusters.
        """
        parser = GodotDataParser()
        graph = parser.parse_dot_file(CLUSTER_GRAPH)
#        self.failUnless(graph.name == "testG")
#        graph.configure_traits()
#        graph.save_to_file("/tmp/clust.dot")
        print graph.clusters[0]


#    def test_parse_colors(self):
#        """ Test parsing of a graph with colors.
#        """
#        parser = GodotDataParser()
#        graph = parser.parse_dot_file(COLORS_GRAPH)


if __name__ == "__main__":
    unittest.main()

# EOF -------------------------------------------------------------------------

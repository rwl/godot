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

""" Defines a parser of Graphviz dot data.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from dot2tex.dotparsing \
    import DotDataParser, ADD_NODE, ADD_EDGE, ADD_GRAPH_TO_NODE_EDGE, \
    ADD_NODE_TO_GRAPH_EDGE, ADD_GRAPH_TO_GRAPH_EDGE, ADD_SUBGRAPH, \
    SET_DEF_NODE_ATTR, SET_DEF_EDGE_ATTR, SET_DEF_GRAPH_ATTR, SET_GRAPH_ATTR

from graph import Graph
from subgraph import Subgraph
from cluster import Cluster
from node import Node
from edge import Edge

#------------------------------------------------------------------------------
#  "GodotDataParser" class:
#------------------------------------------------------------------------------

class GodotDataParser(DotDataParser):
    """ Parses Graphviz dot data.
    """

    def parse_dot_file(self, file_or_filename):
        """ Returns a graph given a file or a filename.
        """
        if isinstance(file_or_filename, basestring):
            file = None
            try:
                file = open(file_or_filename, "rb")
                data = file.read()
            except:
                print "Could not open %s." % file_or_filename
                return None
            finally:
                if file is not None:
                    file.close()
        else:
            file = file_or_filename
            data = file.read()

        return self.parse_dot_data(data)


    def build_top_graph(self,tokens):
        """ Build a Godot graph instance from parsed data.
        """
        # Get basic graph information.
        strict = tokens[0] == 'strict'
        graphtype = tokens[1]
        directed = graphtype == 'digraph'
        graphname = tokens[2]
        # Build the graph
        graph = Graph(ID=graphname, strict=strict, directed=directed)
        self.graph = self.build_graph(graph, tokens[3])


    def build_graph(self, graph, tokens):
        """ Builds a Godot graph.
        """
        subgraph = None

        for element in tokens:
            cmd = element[0]
            if cmd == ADD_NODE:
                cmd, nodename, opts = element
                graph.add_node(nodename, **opts)

            elif cmd == ADD_EDGE:
                cmd, src, dest, opts = element
                srcport = destport = ""
                if isinstance(src,tuple):
                    srcport = src[1]
                    src = src[0]
                if isinstance(dest,tuple):
                    destport = dest[1]
                    dest = dest[0]

                graph.add_edge(src, dest, tailport=srcport, headport=destport,
                               **opts)

            elif cmd in [ADD_GRAPH_TO_NODE_EDGE,
                         ADD_GRAPH_TO_GRAPH_EDGE,
                         ADD_NODE_TO_GRAPH_EDGE]:
                cmd, src, dest, opts = element
                srcport = destport = ""

                if isinstance(src,tuple):
                    srcport = src[1]

                if isinstance(dest,tuple):
                    destport = dest[1]

                if not (cmd == ADD_NODE_TO_GRAPH_EDGE):
                    if cmd == ADD_GRAPH_TO_NODE_EDGE:
                        src = subgraph
                    else:
                        src = prev_subgraph
                        dest = subgraph
                else:
                    dest = subgraph

                src_is_graph = isinstance(src, (Subgraph, Cluster))
                dst_is_graph = isinstance(dst, (Subgraph, Cluster))

                if src_is_graph:
                    src_nodes = src.nodes
                else:
                    src_nodes = [src]
                if dst_is_graph:
                    dst_nodes = dst.nodes
                else:
                    dst_nodes = [dst]

                for src_node in src_nodes:
                    for dst_node in dst_nodes:
                        graph.add_edge(from_node=src_node, to_node=dst_node,
                                       tailport=srcport, headport=destport,
                                       **kwds)

            elif cmd == SET_GRAPH_ATTR:
                graph.set( **element[1] )

            elif cmd == SET_DEF_NODE_ATTR:
                graph.default_node.set( **element[1] )

            elif cmd == SET_DEF_EDGE_ATTR:
                graph.default_edge.set( **element[1] )

            elif cmd == SET_DEF_GRAPH_ATTR:
                graph.default_graph.set (**element[1] )

            elif cmd == ADD_SUBGRAPH:
                cmd, name, elements = element
                if subgraph:
                    prev_subgraph = subgraph
                if name.startswith("cluster"):
                    cluster = Cluster(ID=name)
                    cluster = self.build_graph(cluster, elements)
                    graph.add_cluster(cluster)
                else:
                    subgraph = Subgraph(ID=name)
                    subgraph = self.build_graph(subgraph, elements)
                    graph.add_subgraph(subgraph)

        return graph

# EOF -------------------------------------------------------------------------

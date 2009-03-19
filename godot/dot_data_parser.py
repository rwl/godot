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

from dot2tex.dotparsing import DotDataParser

from graph import Graph
from subgraph import Subgraph
from node import Node
from edge import Edge

#------------------------------------------------------------------------------
#  "GodotDataParser" class:
#------------------------------------------------------------------------------

class GodotDataParser(DotDataParser):
    """ Parses Graphviz dot data.
    """

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
                node = Node(ID=nodename, **opts)
                graph.nodes.append(node)

            elif cmd == ADD_EDGE:
                cmd, src, dest, opts = element
                srcport = destport = ""
                if isinstance(src,tuple):
                    srcport = src[1]
                    src = src[0]
                if isinstance(dest,tuple):
                    destport = dest[1]
                    dest = dest[0]

                edge = Edge(from_node=src, to_node=dest,
                            tailport=srcport, headport=destport, **opts)
                graph.edges.append(edge)

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

                src_is_graph = isinstance(src, Subgraph)
                dst_is_graph = isinstance(dst, Subgraph)
                edges = []
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
                        edge = Edge(from_node=src_node, to_node=dst_node,
                                    tailport=srcport, headport=destport,**kwds)
                        edges.append(edge)

                graph.edges.extend(edges)

            elif cmd == SET_GRAPH_ATTR:
                setattr(graph, **element[1])

            elif cmd == SET_DEF_NODE_ATTR:
#                graph.add_default_node_attr(**element[1])
#                defattr = DotDefaultAttr('node',**element[1])
#                graph.allitems.append(defattr)
                raise NotImplementedError

            elif cmd == SET_DEF_EDGE_ATTR:
#                graph.add_default_edge_attr(**element[1])
#                defattr = DotDefaultAttr('edge',**element[1])
#                graph.allitems.append(defattr)
                raise NotImplementedError

            elif cmd == SET_DEF_GRAPH_ATTR:
#                graph.add_default_graph_attr(**element[1])
#                defattr = DotDefaultAttr('graph',**element[1])
#                graph.allitems.append(defattr)
                raise NotImplementedError

            elif cmd == ADD_SUBGRAPH:
                cmd, name, elements = element
                if subgraph:
                    prev_subgraph = subgraph
                subgraph = Subgraph(ID=name)
                subgraph = self.build_graph(subgraph, elements)
                graph.subgraphs.append(subgraph)

        return graph

# EOF -------------------------------------------------------------------------

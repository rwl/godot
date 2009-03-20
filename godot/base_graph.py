#------------------------------------------------------------------------------
#  Copyright (c) 2008 Richard W. Lincoln
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

""" Defines a base class for many graphs. """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, Str, List, Instance, Bool, Property, Constant, \
    ReadOnly, Dict, TraitListEvent

from enthought.enable.api \
    import Container

from node import Node
from edge import Edge
from common import id_trait, Alias

from dot_writer import write_dot_graph

#------------------------------------------------------------------------------
#  "BaseGraph" class:
#------------------------------------------------------------------------------

class BaseGraph(HasTraits):
    """ Defines a representation of a graph in Graphviz's dot language """

    #--------------------------------------------------------------------------
    #  Trait definitions.
    #--------------------------------------------------------------------------

    # Optional unique identifier.
    ID = id_trait

    # Synonym for ID.
    name = Alias("ID", desc="synonym for ID") # Used by InstanceEditor

    # Main graph nodes.
    nodes = List( Instance(Node) )

    # Map if node IDs to node objects.
    id_node_map = Dict

    # Graph edges.
    edges = List(Instance(Edge))

    # Separate layout regions.
    subgraphs = List(Instance("godot.subgraph.Subgraph"))

    # Clusters are encoded as subgraphs whose names have the prefix 'cluster'.
    clusters = List(Instance("godot.cluster.Cluster"))

    #--------------------------------------------------------------------------
    #  Enable trait definitions.
    #--------------------------------------------------------------------------

    # Container of graph components.
    component = Instance(Container, desc="container of graph components.")

    #--------------------------------------------------------------------------
    #  Xdot trait definitions:
    #--------------------------------------------------------------------------

    # For a given graph object, one will typically a draw directive before the
    # label directive. For example, for a node, one would first use the
    # commands in _draw_ followed by the commands in _ldraw_.
    _draw_ = Str(desc="xdot drawing directive")

    # Label draw directive.
    _ldraw_ = Str(desc="xdot label drawing directive")

    #--------------------------------------------------------------------------
    #  "object" interface:
    #--------------------------------------------------------------------------

    def __len__(self):
        """ Return the order of the graph when requested by len().

            @rtype:  number
            @return: Size of the graph.
        """
        return len(self.nodes)


    def __iter__(self):
        """ Return a iterator passing through all nodes in the graph.

            @rtype:  iterator
            @return: Iterator passing through all nodes in the graph.
        """
        for each in self.nodes:
            yield each


    def __getitem__(self, node):
        """ Return a iterator passing through all neighbours of the given node.

            @rtype:  iterator
            @return: Iterator passing through all neighbours of the given node.
        """
        for each_edge in self.edges:
            if (each_edge.tail_node == node) or (each_edge.head_node == node):
                yield each_edge

    #--------------------------------------------------------------------------
    #  Public interface:
    #--------------------------------------------------------------------------

    def add_node(self, node_or_ID, **kwds):
        """ Adds a node to the graph.
        """
        if not isinstance(node_or_ID, Node):
            nodeID = str( node_or_ID )
            if nodeID in self.nodes:
                node = self.nodes[ self.nodes.index(nodeID) ]
            else:
                node = self.clone_traits(self.default_node, copy="deep")
                node.ID = nodeID
                self.nodes.append( node )
        else:
            node = node_or_ID
            if node in self.nodes:
                node = self.nodes[ self.nodes.index(node_or_ID) ]
            else:
                self.nodes.append( node )

        node.set( **kwds )

        return node


    def delete_node(self, node_or_ID):
        """ Removes a node from the graph.
        """
        if isinstance(node_or_ID, Node):
            name = node.ID
        else:
            name = node_or_ID

        self.nodes = [n for n in self.nodes if n.ID != name]


    def get_node(self, ID):
        """ Returns the node with the given ID or None.
        """
        for node in self.nodes:
            if node.ID == ID:
                return node
        else:
            return None


    def add_edge(self, tail_node_or_ID, head_node_or_ID, **kwds):
        """ Adds an edge to the graph.
        """
        tail_node = self.add_node(tail_node_or_ID)
        head_node = self.add_node(head_node_or_ID)

        # Only top level graphs are directed and/or strict.
        if "directed" in self.trait_names():
            directed = self.directed
        else:
            directed = False

        edge = Edge(tail_node, head_node, directed, **kwds)

        if "strict" in self.trait_names():
            if not self.strict:
                self.edges.append(edge)
            else:
                raise NotImplementedError
        else:
            self.edges.append(edge)


    def to_string(self):
        """ Returns a string representation of the graph in dot language. It
            will return the graph and all its subelements in string form.
        """
        return write_dot_graph(self)

    #--------------------------------------------------------------------------
    #  Trait initialisers:
    #--------------------------------------------------------------------------

    def _component_default(self):
        """ Trait initialiser.
        """
        return Container(fit_window=False, auto_size=True)

    #--------------------------------------------------------------------------
    #  "BaseGraph" interface:
    #--------------------------------------------------------------------------

#    @on_trait_change("nodes,nodes_items")
#    def remove_duplicates(self, new):
#        """ Ensures node ID uniqueness.
#        """
#        if isinstance(new, TraitListEvent):
#            old = event.removed
#            new = event.added
#
#        set = {}
#        self.set( trait_change_notify = False,
#                  nodes = [set.setdefault(e, e) for e in new if e not in set] )


    @on_trait_change("nodes,nodes_items")
    def _set_node_lists(self, new):
        """ Maintains each edge's list of available nodes.
        """
        for edge in self.edges:
            edge._nodes = self.nodes


#    @on_trait_change("nodes,nodes_items")
#    def _manage_id_node_map(self, obj, name, old, new):
#        """ Maintains a dictionary mapping node IDs to nodes.
#        """
#        if isinstance(new, TraitListEvent):
#            old = event.removed
#            new = event.added
#        else:
#            self.id_node_map = {}
#
#        for new_node in new:
#            self.id_node_map[new_node.ID] = new_node
#
#        for old_node in old:
#            try:
#                self.id_node_map.pop(node.ID)
#            except KeyError:
#                print "Removed node not found in ID map. Updating."
#                self._update_id_node_map()


    def _nodes_items_changed(self, event):
        """ Handles addition and removal of nodes.
        """
        # Add new nodes to the canvas.
        from enthought.enable.primitives.api import Box
        from enthought.enable.tools.api import MoveTool

        for node in event.added:
            box = Box(color="steelblue", border_color="darkorchid",
                border_size=1, bounds=[50, 50], position=[10, 10])
            box.tools.append(MoveTool(box))
            self.component.add(box)
            self.component.add(node.component)

        self.component.request_redraw()


#    def _update_id_node_map(self):
#        """ Sets the map of node IDs to nodes.
#        """
#        d = {}
#        for node in self.nodes:
#            d[node.ID] = node
#        self.id_node_map = d

# EOF -------------------------------------------------------------------------

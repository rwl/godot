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

""" Defines the graph editor factory for all traits user interface toolkits.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Any, Dict, Bool, Tuple, Int, \
    List, Instance, Str, Enum, Callable, Any, Class

from enthought.traits.ui.editor_factory \
    import EditorFactory

from enthought.traits.ui.helper \
    import Orientation

from enthought.etsconfig.api \
    import ETSConfig

if ETSConfig.toolkit == "wx":
    from enthought.traits.ui.wx.editor import Editor
elif ETSConfig.toolkit == "qt4":
    from enthought.traits.ui.qt4.editor import Editor
else:
    from enthought.traits.ui.editor import Editor

from godot.api \
    import Graph

#------------------------------------------------------------------------------
#  'GraphCanvas' class:
#------------------------------------------------------------------------------

class GraphCanvas ( HasPrivateTraits ):
    """ Defines a representation of a graph canvas for use by the graph editor
        and the graph editor factory classes.
    """

    # Names of list traits whose elements are represented as nodes.
    node_children = List(Str)

    # Names of the list traits whose elements are represented as edges.
    edge_children = List(Str)

#------------------------------------------------------------------------------
#  'GraphNode' class:
#------------------------------------------------------------------------------

class GraphNode ( HasPrivateTraits ):
    """ Defines a representation of a graph node for use by the graph editor
        and the graph editor factory classes.
    """

    # Name of the context object's trait that contains the object being
    # represented by the node.
#    child_of = Str

    # Either the name of a trait containing a label, or a constant label, if
    # the string starts with '='.
    label = Str

    # Function for formatting the label.
    formatter = Callable

    # List of object classes and/or interfaces that the node applies to.
    node_for = List( Any )

    # Dot attributes to be applied to the node.
    dot_attr = Dict(Str, Any)

    # Text to be displayed as a tip for usage.
    tooltip = Str

    # Called when the graph node is double-clicked.
    on_dclick = Callable

    #---------------------------------------------------------------------------
    #  Gets the label to display for a specified object:
    #---------------------------------------------------------------------------

    def get_label ( self, object ):
        """ Gets the label to display for a specified object.
        """
        label = self.label
        if label[:1] == '=':
            return label[1:]

        label = xgetattr( object, label, '' )

        if self.formatter is None:
            return label

        return self.formatter( object, label )

    #---------------------------------------------------------------------------
    #  Sets the label for a specified object:
    #---------------------------------------------------------------------------

    def set_label ( self, object, label ):
        """ Sets the label for a specified object.
        """
        label_name = self.label
        if label_name[:1] != '=':
            xsetattr( object, label_name, label )

    #---------------------------------------------------------------------------
    #  Sets up/Tears down a listener for 'label changed' on a specified object:
    #---------------------------------------------------------------------------

    def when_label_changed ( self, object, listener, remove ):
        """ Sets up or removes a listener for the label being changed on a
            specified object.
        """
        label = self.label
        if label[:1] != '=':
            object.on_trait_change( listener, label, remove = remove,
                                    dispatch = 'ui' )

#------------------------------------------------------------------------------
#  'GraphEdge' class:
#------------------------------------------------------------------------------

class GraphEdge ( HasPrivateTraits ):
    """ Defines a representation of a graph edge for use by the graph editor
        and the graph editor factory classes.
    """

#    head_nodes = List( Instance(HasTraits) )
    head_name = Str

#    tail_nodes = List( Instance(HasTraits) )
    tail_name = Str

    # List of object classes and/or interfaces that the edge applies to.
    edge_for = List( Any )

    # Dot attributes to be applied to the edge.
    dot_attr = Dict(Str, Any)

#------------------------------------------------------------------------------
#  'SimpleGraphEditor' class:
#------------------------------------------------------------------------------

class SimpleGraphEditor ( Editor ):
    """ Simple style of graph editor.
    """

    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    # Currently selected object.
    selected = Any

    #-- Private Traits --------------------------------------------------------

    _graph = Instance(Graph)

    #--------------------------------------------------------------------------
    #  Finishes initialising the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initialising the editor by creating the underlying toolkit
            widget.
        """
        self._graph = graph = Graph()
        ui = graph.edit_traits(parent=parent, kind="panel")
        self.control = ui.control

    #--------------------------------------------------------------------------
    #  Disposes of the contents of an editor:
    #--------------------------------------------------------------------------

    def dispose ( self ):
        """ Disposes of the contents of an editor.
        """
        super(SimpleGraphEditor, self).dispose()

    #--------------------------------------------------------------------------
    #  Handles an error that occurs while setting the object's trait value:
    #--------------------------------------------------------------------------

    def error ( self, excp ):
        """ Handles an error that occurs while setting the object's trait
            value.
        """
        pass

    #--------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #--------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        object = self.value
        # Graph the new object...
        canvas = self.factory.canvas
        if canvas is not None:
            for nodes_name in canvas.node_children:
                node_children = getattr(object, nodes_name)
                self._add_nodes(node_children)

            for edges_name in canvas.edge_children:
                edge_children = getattr(object, edges_name)
                self._add_edges(edge_children)

        # ...then listen for changes.
        self._add_listeners()

    #--------------------------------------------------------------------------
    #  Adds the event listeners for a specified object:
    #--------------------------------------------------------------------------

    def _add_listeners ( self ):
        """ Adds the event listeners for a specified object.
        """
        object = self.value
        canvas = self.factory.canvas
        if canvas is not None:
            for name in canvas.node_children:
                object.on_trait_change(self._nodes_replaced, name)
                object.on_trait_change(self._nodes_changed, name + "_items")

            for name in canvas.edge_children:
                object.on_trait_change(self._edges_replaced, name)
                object.on_trait_change(self._edges_changed, name + "_items")
        else:
            raise ValueError("Graph canvas not set for graph editor.")

#        node.when_label_changed( object, self._label_updated, False )

    #--------------------------------------------------------------------------
    #  Node event handlers:
    #--------------------------------------------------------------------------

    def _nodes_replaced(self, object, name, old, new):
        """ Handles a list of nodes being set.
        """
        self._delete_nodes(old)
        self._add_nodes(new)


    def _nodes_changed(self, object, name, undefined, event):
        """ Handles addition and removal of nodes.
        """
        self._delete_nodes(event.removed)
        self._add_nodes(event.added)


    def _add_nodes(self, features):
        """ Adds a node to the graph for each item in 'features' using
            the GraphNodes from the editor factory.
        """
        graph = self._graph

        if graph is not None:
            for feature in features:
                for graph_node in self.factory.nodes:
                    if feature.__class__ in graph_node.node_for:
                        graph.add_node( id(feature), **graph_node.dot_attr )
                        break

        graph.arrange_all()


    def _delete_nodes(self, features):
        """ Removes the node corresponding to each item in 'features'.
        """
        graph = self._graph

        if graph is not None:
            for feature in features:
                graph.delete_node( id(feature) )

        graph.arrange_all()

    #--------------------------------------------------------------------------
    #  Edge event handlers:
    #--------------------------------------------------------------------------

    def _edges_replaced(self, object, name, old, new):
        """ Handles a list of edges being set.
        """
        self._delete_edges(old)
        self._add_edges(new)


    def _edges_changed(self, object, name, undefined, event):
        """ Handles addition and removal of edges.
        """
        self._delete_edges(event.removed)
        self._add_edges(event.added)


    def _add_edges(self, features):
        """ Adds an edge to the graph for each item in 'features' using
            the GraphEdges from the editor factory.
        """
        graph = self._graph

        if graph is not None:
            for feature in features:
                for graph_edge in self.factory.edges:
                    if feature.__class__ in graph_edge.edge_for:
                        tail_feature = getattr(feature, graph_edge.tail_name)
                        head_feature = getattr(feature, graph_edge.head_name)

                        graph.add_edge( id(tail_feature), id(head_feature),
                            **graph_edge.dot_attr )

                        break

        graph.arrange_all()


    def _delete_edges(self, features):
        """ Removes the node corresponding to each item in 'features'.
        """
        graph = self._graph

        if graph is not None:
            for feature in features:
                for graph_edge in self.factory.edges:
                    if feature.__class__ in graph_edge.edge_for:
                        tail_feature = getattr(feature, graph_edge.tail_name)
                        head_feature = getattr(feature, graph_edge.head_name)

                        graph.delete_edge( id(tail_feature), id(head_feature) )

        graph.arrange_all()

#------------------------------------------------------------------------------
#  'ToolkitEditorFactory' class:
#------------------------------------------------------------------------------

class ToolkitEditorFactory ( EditorFactory ):
    """ Editor factory for graph editors.
    """
    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    canvas = Instance( GraphCanvas )

    # Graph node definitions.
    nodes = List( Instance(GraphNode) )

    # Graph edge definitions.
    edges = List( Instance(GraphEdge) )

    # Called when a graph element is selected.
    on_select = Callable

    #--------------------------------------------------------------------------
    #  Property getters:
    #--------------------------------------------------------------------------

    def _get_simple_editor_class(self):
        """ Returns the editor class to use for "simple" style views.
        """
        return SimpleGraphEditor


# Define the GraphEditor class.
GraphEditor = ToolkitEditorFactory

# EOF -------------------------------------------------------------------------

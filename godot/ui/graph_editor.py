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
    List, Instance, Str, Enum, Callable, Any

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
#  'GraphNode' class:
#------------------------------------------------------------------------------

class GraphNode ( HasPrivateTraits ):
    """ Defines a representation of a graph node for use by the graph editor
        and the graph editor factory classes.
    """

    # Name of the context object's trait that contains the object being
    # represented by the node.
    child_of = Str

    # Either the name of a trait containing a label, or a constant label, if
    # the string starts with '='.
    label = Str

    # Function for formatting the label.
    formatter = Callable

    # List of object classes and/or interfaces that the node applies to
    node_for = List( Any )

    # Dot attributes to be applied to the node node.
    dot_attr = Dict(Str, Any)

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
        factory = self.factory # GraphEditor
        ui      = self.ui
        object  = self.object  # ViewModel
        name    = self.name    # Trait name
        desc    = self.description

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
        self._add_listeners()

    #--------------------------------------------------------------------------
    #  Adds the event listeners for a specified object:
    #--------------------------------------------------------------------------

    def _add_listeners ( self ):
        """ Adds the event listeners for a specified object.
        """
        canvas = self.value
        print "CANVAS:", canvas
        for node in self.factory.nodes:
            print "CHILD OF:", node.child_of
            canvas.on_trait_change(self._nodes_replaced, node.child_of)
            canvas.on_trait_change(self._nodes_changed, node.child_of+"_items")

#        node.when_label_changed( object, self._label_updated, False )


    def _nodes_replaced(self, object, name, old, new):
        """ Handles a list of nodes being set.
        """
        print "Replaced:", object, name, old, new

        graph = self._graph

        graph_node = None
        for gn in self.factory.nodes:
            if gn.child_of == name:
                graph_node = gn
                break

        if graph is not None:
            for each_old in old:
                graph.delete_node( id(each_old) )

            for each_new in new:
                if graph_node is not None:
                    node_attr = graph_node.dot_attr
                else:
                    node_attr = {}

                node = graph.add_node( id(each_new), **node_attr )


    def _nodes_changed(self, object, name, undefined, event):
        """ Handles addition and removal of nodes.
        """
        print "Changed:", object, name, undefined, event

#------------------------------------------------------------------------------
#  'ToolkitEditorFactory' class:
#------------------------------------------------------------------------------

class ToolkitEditorFactory ( EditorFactory ):
    """ Editor factory for graph editors.
    """
    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    # Supported GraphNode objects.
    nodes = List( GraphNode )

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

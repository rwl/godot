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

""" Defines a tree editor for Godot graphs.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.traits.api import Str
from enthought.traits.ui.api import TreeEditor, TreeNode, View, Item

from godot.base_graph import BaseGraph
from godot.api import Graph, Subgraph, Cluster, Node, Edge

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

IMAGE_PATH = ""

#------------------------------------------------------------------------------
#  "BaseGraphTreeNode" class:
#------------------------------------------------------------------------------

class BaseGraphTreeNode(TreeNode):
    """ Defines an abstract tree node for Godot graph objects.
    """

    #--------------------------------------------------------------------------
    #  "TreeNode" interface:
    #--------------------------------------------------------------------------

    # Name of a trait containing a label.
    label = Str( "ID" )

    # Text to display when hovering the mouse over the node.
    tooltip = Str( "=Graph" )

    # List of object classes than can be added or copied.
    add = [ Subgraph, Cluster, Node, Edge ]

    # List of object classes that can be moved.
    move = [ Subgraph, Cluster, Node, Edge ]

    # Resource path used to locate the node icon.
    icon_path = Str(IMAGE_PATH)

    #--------------------------------------------------------------------------
    #  End "RegulationSchedule" user definitions:
    #--------------------------------------------------------------------------

    def allows_children ( self, object ):
        """ Returns whether this object can have children.
        """
        return True


    def get_children ( self, object ):
        """ Gets the object's children.
        """
        children = []
        children.extend( object.subgraphs )
        children.extend( object.clusters )
        children.extend( object.nodes )
        children.extend( object.edges )
        return children


    def append_child ( self, object, child ):
        """ Appends a child to the object's children.
        """
        if isinstance( child, Subgraph ):
            object.subgraphs.append( child )

        elif isinstance( child, Cluster ):
            object.clusters.append( child )

        elif isinstance( child, Node ):
            object.nodes.append( child )

        elif isinstance( child, Edge ):
            object.edges.append( child )

        else:
            pass


    def insert_child ( self, object, index, child ):
        """ Inserts a child into the object's children.
        """
        if isinstance( child, Subgraph ):
            object.subgraphs.insert( index, child )

        elif isinstance( child, Cluster ):
            object.clusters.insert( index, child )

        elif isinstance( child, Node ):
            object.nodes.insert( index, child )

        elif isinstance( child, Edge ):
            object.edges.insert( index, child )

        else:
            pass


    def delete_child ( self, object, index ):
        """ Deletes a child at a specified index from the object's children.
        """
        if isinstance( child, Subgraph ):
            object.subgraphs.pop(index)

        elif isinstance( child, Cluster ):
            object.clusters.pop( index )

        elif isinstance( child, Node ):
            object.nodes.pop( index )

        elif isinstance( child, Edge ):
            object.edges.pop( index )

        else:
            pass


    def when_children_replaced ( self, object, listener, remove ):
        """ Sets up or removes a listener for children being replaced on a
            specified object.
        """
        object.on_trait_change( listener, "subgraphs", remove = remove,
                                dispatch = "fast_ui" )
        object.on_trait_change( listener, "clusters", remove = remove,
                                dispatch = "fast_ui" )
        object.on_trait_change( listener, "nodes", remove = remove,
                                dispatch = "fast_ui" )
        object.on_trait_change( listener, "edges", remove = remove,
                                dispatch = "fast_ui" )


    def when_children_changed ( self, object, listener, remove ):
        """ Sets up or removes a listener for children being changed on a
            specified object.
        """
        object.on_trait_change( listener, "subgraphs_items",
                                remove = remove, dispatch = "fast_ui" )
        object.on_trait_change( listener, "clusters_items",
                                remove = remove, dispatch = "fast_ui" )
        object.on_trait_change( listener, "nodes_items",
                                remove = remove, dispatch = "fast_ui" )
        object.on_trait_change( listener, "edges_items",
                                remove = remove, dispatch = "fast_ui" )


    def dclick ( self, object ):
        """ Handles an object being double-clicked.
        """
        if object is not None:
            object.edit_traits(kind="livemodal")
            return None

        return True

#------------------------------------------------------------------------------
#  "GraphTreeNode" class:
#------------------------------------------------------------------------------

class GraphTreeNode(BaseGraphTreeNode):
    """ Defines a tree node for Graph.
    """

    # Name to use for a new instance.
    name = Str( "Graph" )

    # List of object classes and/or interfaces that the node applies to.
    node_for = [ Graph ]

    # Name of group item icon.
    icon_group = Str( "" )

    # Name of opened group item icon.
    icon_open = Str( "dot" )

#------------------------------------------------------------------------------
#  "SubgraphTreeNode" class:
#------------------------------------------------------------------------------

class SubgraphTreeNode(BaseGraphTreeNode):
    """ Defines a tree node for Subgraph.
    """

    # Name to use for a new instance.
    name = Str( "Subgraph" )

    # List of object classes and/or interfaces that the node applies to.
    node_for = [ Subgraph ]

    # Name of group item icon.
    icon_group = Str( "subgraph" )

    # Name of opened group item icon.
    icon_open = Str( "subgraph" )

#------------------------------------------------------------------------------
#  "ClusterTreeNode" class:
#------------------------------------------------------------------------------

class ClusterTreeNode(BaseGraphTreeNode):
    """ Defines a tree node for Cluster.
    """

    # Name to use for a new instance.
    name = Str( "Cluster" )

    # List of object classes and/or interfaces that the node applies to.
    node_for = [ Cluster ]

    # Name of group item icon.
    icon_group = Str( "cluster" )

    # Name of opened group item icon.
    icon_open = Str( "cluster" )

#------------------------------------------------------------------------------
#  Graph tree editor:
#------------------------------------------------------------------------------

no_view = View()

graph_tree_editor = TreeEditor(
    nodes = [
        GraphTreeNode(),
        SubgraphTreeNode(),
        ClusterTreeNode(),
#        TreeNode(node_for=[Graph], auto_open=True, children="", label="ID",
#            icon_item="graph", rename_me=True),
#        TreeNode(node_for=[Graph], auto_open=False, children="subgraphs",
#            label="=Subgraphs", add=[Subgraph]),
#        TreeNode(node_for=[Graph], auto_open=False, children="clusters",
#            label="=Clusters", add=[Cluster]),
#        TreeNode(node_for=[Graph], auto_open=True, children="nodes",
#            label="=Nodes", add=[Node]),
#        TreeNode(node_for=[Graph], auto_open=True, children="edges",
#            label="=Edges"),
#
#        TreeNode(node_for=[Subgraph], label="ID", icon_item="subgraph"),
#        TreeNode(node_for=[Subgraph], auto_open=False, children="subgraphs",
#            label="=Subgraphs", add=[Subgraph]),
#        TreeNode(node_for=[Subgraph], auto_open=False, children="clusters",
#            label="=Clusters", add=[Cluster]),
#        TreeNode(node_for=[Subgraph], auto_open=False, children="nodes",
#            label="=Nodes", add=[Node]),
#        TreeNode(node_for=[Subgraph], children="edges", label="=Edges"),
#
#        TreeNode(node_for=[Cluster], label="ID", icon_item="cluster"),
#        TreeNode(node_for=[Cluster], auto_open=False, children="subgraphs",
#            label="=Subgraphs", add=[Subgraph]),
#        TreeNode(node_for=[Cluster], auto_open=False, children="clusters",
#            label="=Clusters", add=[Cluster]),
#        TreeNode(node_for=[Cluster], auto_open=False, children="nodes",
#            label="=Nodes", add=[Node]),
#        TreeNode(node_for=[Cluster], children="edges", label="=Edges"),

        TreeNode(node_for=[Node], label="ID", icon_item="node"),
        TreeNode(node_for=[Edge], label="name", icon_item="edge")
    ],
    orientation="vertical", editable=False,# hide_root=True,
    on_dclick=lambda obj: obj.edit_traits(kind="livemodal"),
#    selected="selected_graph"
)

# EOF -------------------------------------------------------------------------

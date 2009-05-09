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

""" Defines test cases for Godot's Traits UI graph editor.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import unittest

from enthought.traits.api \
    import HasTraits, ListInstance, Str, Instance, List, Button

from enthought.traits.ui.api \
    import View, Item, Group, ModelView, TreeEditor, TreeNode, HGroup

from godot.ui.api \
    import GraphEditor, GraphCanvas, GraphNode, GraphEdge

#------------------------------------------------------------------------------
#  "DomainNode" class:
#------------------------------------------------------------------------------

class OtherNode(HasTraits):
    name = Str("othernode")

class DomainNode(HasTraits):
    name = Str("graphnode")
    other = Instance(OtherNode)

class OtherNode(HasTraits):
    name = Str("othernode")

class DomainEdge(HasTraits):
    name = Str("graphedge")
    source = Instance(DomainNode)
    target = Instance(DomainNode)

class DomainModel(HasTraits):
    nodes = List( Instance(DomainNode) )
    edges = List( Instance(DomainEdge) )
    other_nodes = List( Instance(OtherNode) )

tree_editor = TreeEditor(
    nodes = [
        TreeNode(node_for=[DomainModel], label="=Model"),
        TreeNode(node_for=[DomainModel], label="=Nodes", children="nodes",
            add=[DomainNode]),
        TreeNode(node_for=[DomainModel], label="=Edges", children="edges",
            add=[DomainEdge]),
        TreeNode(node_for=[DomainModel], label="=Other Nodes",
            children="other_nodes", add=[OtherNode]),
        TreeNode(node_for=[DomainNode], label="name"),
        TreeNode(node_for=[DomainEdge], label="name"),
        TreeNode(node_for=[OtherNode], label="name")
    ], editable=False
)

graph_editor = GraphEditor(
    canvas = GraphCanvas( node_children=["nodes", "other_nodes"],
                          edge_children=["edges"] ),
    nodes = [
        GraphNode( node_for = [DomainNode],
                   label    = "name",
                   dot_attr = {"shape": "circle"}
        ),
        GraphNode( node_for = [OtherNode],
                   label    = "name",
                   dot_attr = {"shape": "triangle"}
        )
    ],
    edges = [
        GraphEdge( edge_for  = [DomainEdge],
                   head_name = "target",
                   tail_name = "source" )
    ]
)

class DomainViewModel(ModelView):
    add_node = Button
    del_node = Button("Remove node")

    traits_view = View(
        HGroup(
            Item("model", editor=tree_editor, show_label=False),
            Item("model", editor=graph_editor, show_label=False),
    #        Item("add_node", show_label=False),
    #        Item("del_node", show_label=False, enabled_when="model.nodes"),
            layout="split", id=".splitter"
        ),
        resizable=True,
        id="godot.editor_test.domain_view_model",
        close_result=True)

    def _add_node_fired(self):
        node = DomainNode(name="new")
        self.model.nodes.append(node)

    def _del_node_fired(self):
        if self.model.nodes:
            popped = self.model.nodes.pop()
            print "POPPED:", popped

#------------------------------------------------------------------------------
#  "GraphEditorTestCase" class:
#------------------------------------------------------------------------------

class GraphEditorTestCase(unittest.TestCase):
    """ Defines a test case for Godot's Traits UI graph editor.
    """

    view_model = Instance(DomainViewModel)

    #--------------------------------------------------------------------------
    #  "TestCase" interface
    #--------------------------------------------------------------------------

    def setUp(self):
        """ Prepares the test fixture before each test method is called.
        """
        node1 = DomainNode(name="node1")
        node2 = DomainNode(name="node2")
        edge1 = DomainEdge(source=node1, target=node2)
        model = DomainModel(nodes=[node1, node2], edges=[edge1])

        self.view_model = DomainViewModel(model=model)


    def test_create_editor(self):
        """ Test creation of a graph editor.
        """
        self.view_model.configure_traits()


if __name__ == "__main__":
    unittest.main()

# EOF -------------------------------------------------------------------------

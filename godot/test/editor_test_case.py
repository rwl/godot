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
    import HasTraits, ListInstance, Str, Instance, List

from enthought.traits.ui.api \
    import View, Item, Group, ModelView

from godot.ui.api \
    import GraphEditor, GraphNode

#------------------------------------------------------------------------------
#  "DomainNode" class:
#------------------------------------------------------------------------------

class DomainNode(HasTraits):
    name = Str("node")

class OtherNode(HasTraits):
    name = Str("other")

class DomainEdge(HasTraits):
    source = Instance(DomainNode)
    target = Instance(DomainNode)

class DomainModel(HasTraits):
    nodes = List( Instance(DomainNode) )
    edges = List( Instance(DomainEdge) )
    other_nodes = List( Instance(OtherNode) )

graph_editor = GraphEditor(
    nodes = [
        GraphNode( child_of = "nodes",
                   label    = "name",
                   node_for = [DomainNode]
        ),
        GraphNode( child_of = "other_nodes",
                   label    = "name",
                   node_for = [OtherNode]
        )
    ]
)

class DomainViewModel(ModelView):
    traits_view = View( Item("model", editor=graph_editor) )

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

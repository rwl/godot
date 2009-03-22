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
    import Any, Dict, Bool, Tuple, Int, List, Instance, Str, Enum

from enthought.traits.ui.editor_factory \
    import EditorFactory

from enthought.traits.ui.helper \
    import Orientation

from enthought.traits.ui.editor \
    import Editor

from godot.graph \
    import Graph

#------------------------------------------------------------------------------
#  'SimpleGraphEditor' class:
#------------------------------------------------------------------------------

class SimpleGraphEditor ( Editor ):
    """ Simple style of graph editor.
    """

    #--------------------------------------------------------------------------
    #  Finishes initialising the editor by creating the underlying toolkit
    #  widget:
    #--------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initialising the editor by creating the underlying toolkit
            widget.
        """
        graph = Graph()
        ui = graph.edit_traits(parent=parent, kind="panel")
        self.control = ui.control

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        pass

#------------------------------------------------------------------------------
#  'ToolkitEditorFactory' class:
#------------------------------------------------------------------------------

class ToolkitEditorFactory ( EditorFactory ):
    """ Editor factory for graph editors.
    """
    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    # Supported TreeNode objects
    nodes = List( GraphNode )

    #--------------------------------------------------------------------------
    #  Property getters
    #--------------------------------------------------------------------------

    def _get_simple_editor_class(self):
        """ Returns the editor class to use for "simple" style views.
        The default implementation tries to import the SimpleEditor class in the
        editor file in the backend package, and if such a class is not to found
        it returns the SimpleEditor class defined in editor_factory module in
        the backend package.

        """
        try:
            SimpleEditor = self._get_toolkit_editor('SimpleEditor')
        except:
            SimpleEditor = toolkit_object('editor_factory:SimpleEditor')
        return SimpleEditor

# EOF -------------------------------------------------------------------------

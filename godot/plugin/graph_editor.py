#------------------------------------------------------------------------------
# Copyright (C) 2009 Richard W. Lincoln
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANDABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#------------------------------------------------------------------------------

""" Defines a graph editor.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from os.path import exists, basename, join, dirname

from enthought.traits.api \
    import HasTraits, Code, Instance, Str, Adapter, adapts, AdaptsTo

from enthought.io.api import File
from enthought.pyface.workbench.api import TraitsUIEditor
from enthought.traits.ui.api import View, Item, Group
from enthought.traits.ui.api import ImageEditor as ImageTraitEditor
from enthought.pyface.image_resource import ImageResource

from puddle.resource.api \
    import IResource, ResourceEditor, ResourcePlugin, Editor

from godot.api import Graph, parse_dot_file

from dot_adapter import DotFileIResourceAdapter

IMAGE_LOCATION = join(dirname(__file__), "..", "ui", "images")

#------------------------------------------------------------------------------
#  "GraphEditor" class:
#------------------------------------------------------------------------------

class GraphEditor(ResourceEditor):
    """ A graph editor.
    """

    #--------------------------------------------------------------------------
    #  "GraphEditor" interface:
    #--------------------------------------------------------------------------

    # Dot file on the file system.
    editor_input = AdaptsTo(IResource)

    # Graph loaded from the resource.
    graph = Instance(Graph)

    # An optional reference to the currently selected object in the editor.
    selected = Instance(HasTraits) # Used by the properties view.

    #--------------------------------------------------------------------------
    #  "TraitsUIEditor" interface.
    #--------------------------------------------------------------------------

    def _name_default(self):
        """ Trait initialiser.
        """
        # 'obj' is a io.File
        self.obj.on_trait_change(self.on_path, "path")

        return basename(self.obj.path)


    def on_path(self, new):
        """ Handle the file path changing.
        """
        self.name = basename(new)
        self.graph = self.editor_input.load()

    #--------------------------------------------------------------------------
    #  "GraphEditor" interface.
    #--------------------------------------------------------------------------

    def _editor_input_default(self):
        """ Trait initialiser.
        """
        return self.obj


    def create_ui(self, parent):
        """ Creates the toolkit-specific control that represents the
            editor. 'parent' is the toolkit-specific control that is
            the editor's parent.
        """
        self.graph = self.editor_input.load()

        view = View(Item(name="graph", style="custom", show_label=False),
            id="godot.graph_editor", kind="live", resizable=True)

        ui = self.edit_traits(view=view, parent=parent, kind="subpanel")

        return ui

    #--------------------------------------------------------------------------
    #  "ResourceEditor" interface:
    #--------------------------------------------------------------------------

    def save(self):
        """ Saves the editor content.
        """
        self.editor_input.save(self.graph)


    def save_as(self):
        """ Saves the editor content to a new file name.
        """
        pass

#------------------------------------------------------------------------------
#  "GraphEditorExtension" class:
#------------------------------------------------------------------------------

class GraphEditorExtension(Editor):
    """ Associates a graph editor with '.dot' file extensions.
    """

    # The object contribution's globally unique identifier.
    id = "godot.plugin.graph_editor"

    # A name that will be used in the UI for this editor
    name = "Graph Editor"

    # An icon that will be used for all resources that match the
    # specified extensions
    image = ImageResource("graph", search_path=[IMAGE_LOCATION])

    # The contributed editor class
    editor_class = "godot.plugin.graph_editor:GraphEditor"

    # The list of file types understood by the editor
    extensions = [".dot", ".xdot"]

    # If true, this editor will be used as the default editor for the type
    default = True

# EOF -------------------------------------------------------------------------

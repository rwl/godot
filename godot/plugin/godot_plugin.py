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

""" Godot plug-in.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.envisage.api import Plugin
from enthought.traits.api import List, Dict, String

#------------------------------------------------------------------------------
#  "GodotPlugin" class:
#------------------------------------------------------------------------------

class GodotPlugin(Plugin):
    """ Godot plug-in.
    """

    # Extension point IDs
    EDITORS = "envisage.resource.editors"

    # Unique plugin identifier
    id = "godot.plugin"

    # Human readable plugin name
    name = "Godot"

    #--------------------------------------------------------------------------
    #  Extensions (Contributions):
    #--------------------------------------------------------------------------

    # Contributed workspace editors:
    editors = List(contributes_to=EDITORS)

    #--------------------------------------------------------------------------
    #  "ImageEditorPlugin" interface:
    #--------------------------------------------------------------------------

    def _editors_default(self):
        """ Trait initialiser.
        """
        from graph_editor import GraphEditorExtension
        from tree_editor import TreeEditorExtension

        return [GraphEditorExtension, TreeEditorExtension]

# EOF -------------------------------------------------------------------------

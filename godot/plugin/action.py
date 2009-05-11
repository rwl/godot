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

""" Defines actions for the Godot plug-in.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from os.path import exists, dirname, join

from enthought.io.api import File
from enthought.pyface.api import ImageResource, FileDialog, CANCEL, OK
from enthought.pyface.action.api import Action as PyFaceAction

from enthought.envisage.ui.action.api import Action, Group, Menu
from enthought.envisage.ui.workbench.api import WorkbenchActionSet

from wizard import NewDotGraphWizard

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

IMAGE_LOCATION = join(dirname(__file__), "..", "ui", "images")

#------------------------------------------------------------------------------
#  "NewDotGraphAction" class:
#------------------------------------------------------------------------------

class NewDotGraphAction(PyFaceAction):
    """ An action for creating a new Dot graph.
    """

    #--------------------------------------------------------------------------
    #  "Action" interface:
    #--------------------------------------------------------------------------

    # A longer description of the action:
    description = "Create a new Dot graph"

    # The action"s name (displayed on menus/tool bar tools etc):
    name = "Graph"

    # A short description of the action used for tooltip text etc:
    tooltip = "Create a Dot graph"

    # The action's image (displayed on tool bar tools etc):
    image = ImageResource("graph", search_path=[IMAGE_LOCATION])

    #--------------------------------------------------------------------------
    #  "Action" interface:
    #--------------------------------------------------------------------------

    def perform(self, event):
        """ Perform the action.
        """
        wizard = NewDotGraphWizard(parent=self.window.control,
            window=self.window, title="New Graph")

        # Open the wizard
        if wizard.open() == OK:
            wizard.finished = True

#------------------------------------------------------------------------------
#  "GodotWorkbenchActionSet" class:
#------------------------------------------------------------------------------

class GodotWorkbenchActionSet(WorkbenchActionSet):
    """ A set of workbench related actions for the Godot plug-in.
    """

    #--------------------------------------------------------------------------
    #  "ActionSet" interface:
    #--------------------------------------------------------------------------

    # The action set"s globally unique identifier.
    id = "godot.plugin.workbench_action_set"

    menus = [ Menu(name="&New", path="MenuBar/File", group="OpenGroup",
        groups=["ContainerGroup", "ComponentGroup", "OtherGroup"]) ]

    actions = [
        Action(path="MenuBar/File/New", group="ComponentGroup",
            class_name="godot.plugin.action:NewDotGraphAction"),

        Action(path="Resource/New", group="ComponentGroup",
            class_name="godot.plugin.action:NewDotGraphAction") ]

# EOF -------------------------------------------------------------------------

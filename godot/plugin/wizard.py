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

""" Defines a wizard for Dot graph resource creation.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from os.path import dirname, join

from enthought.traits.api import Str
from enthought.pyface.api import ImageResource

from puddle.resource.wizard.new_resource_wizard import NewResourceWizard
from puddle.resource.wizard_extension import WizardExtension

from godot.api import Graph

from dot_adapter import DotFileIResourceAdapter

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

IMAGE_LOCATION = join(dirname(__file__), "..", "images")

#------------------------------------------------------------------------------
#  "NewDotGraphWizard" class:
#------------------------------------------------------------------------------

class NewDotGraphWizard(NewResourceWizard):
    """ Defines a wizard for creating new Dot graph resources.
    """

    title = Str("New Dot Graph")

    extensions = [".dot"]

    def get_resource(self, file):
        """ Returns the new adapted resource. Override in subclasses.
        """
        return DotFileIResourceAdapter(file)


    def get_content(self, name):
        """ Returns the content for the new resource. Override in subclasses.
        """
        return Graph(name=name)

#------------------------------------------------------------------------------
#  "NewDotWizardExtension" class:
#------------------------------------------------------------------------------

class NewDotWizardExtension(WizardExtension):
    """ Contributes a new Dot graph creation wizard.
    """
    # The wizard contribution's globally unique identifier.
    id = "godot.new_dot_wizard"

    # Human readable identifier
    name = "Dot Graph"

    # The wizards's image (displayed on selection etc)
    image = ImageResource("graph", search_path=[IMAGE_LOCATION])

    # The class of contributed wizard
    wizard_class = "godot.plugin.wizard:NewDotGraphWizard"

    # A longer description of the wizard's function
    description = "Create a new Dot graph resource"

# EOF -------------------------------------------------------------------------

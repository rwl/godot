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

from enthought.traits.api import Instance, Str, Adapter, adapts
from enthought.io.api import File

from envisage.resource.i_resource import IResource

from godot.api import parse_dot_file

#------------------------------------------------------------------------------
#  "DotFileIResourceAdapter" class:
#------------------------------------------------------------------------------

class DotFileIResourceAdapter(Adapter):
    """ Adapts a "File" with Dot language content to 'IResource'.
    """
    # Declare the interfaces this adapter implements for its client:
    adapts(File, to=IResource, when="adaptee.ext=='.dot'")

    # The object that is being adapted.
    adaptee = Instance(File)

    #--------------------------------------------------------------------------
    #  "IResource" interface:
    #--------------------------------------------------------------------------

    def save(self, obj):
        """ Save to file.
        """
        fd = None
        try:
            fd = open(self.adaptee.absolute_path, "wb")
            obj.save_dot(fd)
        finally:
            if fd is not None:
                fd.close()
#        self.m_time = getmtime(self.adaptee.absolute_path)
        return


    def load(self):
        """ Load the file.
        """
        fd = None
        try:
            obj = parse_dot_file( self.adaptee.absolute_path )
        finally:
            if fd is not None:
                fd.close()
        return obj

# EOF -------------------------------------------------------------------------

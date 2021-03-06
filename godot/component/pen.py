#------------------------------------------------------------------------------
# Copyright (C) 2007 Richard W. Lincoln
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

""" Defines a pen for drawing Graphviz xdot output.

@see: XDot by Jose.R.Fonseca (http://code.google.com/p/jrfonseca/wiki/XDot)

"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.traits.api import HasTraits, Range, Font, Color

from enthought.enable.colors import ColorTrait

#------------------------------------------------------------------------------
#  "Pen" class:
#------------------------------------------------------------------------------

class Pen(HasTraits):
    """ Store pen traits. """

    # Stroke colour.
    color = Color("black", desc="stroke colour")

    # Fill colour.
    fill_color = Color("black", desc="fill colour")

    # Stroke width in points.
    line_width = Range(low=1, high=8, value=1, desc="stroke width in points")

    # Text font.
    font = Font#("14 point Arial")


if __name__ == "__main__":
    pen = Pen(color=0x2B52CB,
              fill_color="255, 128, 64",
              line_width=6,
              font="Arial 14")
    pen.configure_traits()

# EOF -------------------------------------------------------------------------

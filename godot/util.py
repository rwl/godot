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

""" Defines utilities for Godot.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from __future__ import with_statement

import os

from enthought.traits.api import HasTraits, Enum

#------------------------------------------------------------------------------
#  File extension for load/save protocol mapping.
#------------------------------------------------------------------------------

known_extensions = {
    'xml': 'xml',
    'dot': 'dot',
    'pkl': 'pickle' }

#------------------------------------------------------------------------------
#   "Serializable" class:
#------------------------------------------------------------------------------

class Serializable ( HasTraits ):
    """ Class that implements shortcuts to serialize an object.

        Serialization is done by various formats. At the moment, only 'pickle'
        is supported.

        @author: Tom Schaul, tom@idsia.ch; Justin Bayer, bayerj@in.tum.de
    """

    format = Enum("pickle")


    def save_to_file_like(self, flo, format=None, **kwargs):
        """ Save the object to a given file like object in the given format.
        """
        format = self.format if format is None else format
        save = getattr(self, "save_%s" % format, None)
        if save is None:
            raise ValueError("Unknown format '%s'." % format)
        save(flo, **kwargs)


    @classmethod
    def load_from_file_like(cls, flo, format=None):
        """ Load the object to a given file like object with the given
            protocol.
        """
        format = self.format if format is None else format
        load = getattr(cls, "load_%s" % format, None)
        if load is None:
            raise ValueError("Unknown format '%s'." % format)
        return load(flo)


    def save_to_file(self, filename, format=None, **kwargs):
        """ Save the object to file given by filename.
        """
        if format is None:
            # try to derive protocol from file extension
            format = format_from_extension(filename)
        with file(filename, 'wb') as fp:
            self.save_to_file_like(fp, format, **kwargs)


    @classmethod
    def load_from_file(cls, filename, format=None):
        """ Return an instance of the class that is saved in the file with the
            given filename in the specified format.
        """
        if format is None:
            # try to derive protocol from file extension
            format = format_from_extension(filename)
        with file(filename,'rbU') as fp:
            obj = cls.load_from_file_like(fp, format)
            obj.filename = filename
            return obj


    def save_pickle(self, flo, protocol=0):
        pickle.dump(self, flo, protocol)


    @classmethod
    def load_pickle(cls, flo):
        return pickle.load(flo)

#------------------------------------------------------------------------------
#  Tries to infer a protocol from the file extension.
#------------------------------------------------------------------------------

def format_from_extension(fname):
    """ Tries to infer a protocol from the file extension.
    """
    _base, ext = os.path.splitext(fname)
    if not ext:
        return None
    try:
        format = known_extensions[ext.replace('.','')]
    except KeyError:
        format = None
    return format

# EOF -------------------------------------------------------------------------

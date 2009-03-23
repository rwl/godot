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

""" Defines convenient pyparsing constructs and token converters.

    References:
        sparser.py by Tim Cera timcera@earthlink.net
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import re

import itertools

from pyparsing import \
    TokenConverter, oneOf, string, Literal, Group, Word, Optional, Combine, \
    sglQuotedString, dblQuotedString, restOfLine, nums, removeQuotes, Regex, \
    OneOrMore, hexnums, alphas, alphanums, CaselessLiteral, And, NotAny, Or, \
    White, QuotedString

from godot.common import color_schemes

#------------------------------------------------------------------------------
#  Punctuation:
#------------------------------------------------------------------------------

colon  = Literal(":")
lbrace = Literal("{")
rbrace = Literal("}")
lbrack = Literal("[")
rbrack = Literal("]")
lparen = Literal("(")
rparen = Literal(")")
equals = Literal("=")
comma  = Literal(",")
dot    = Literal(".")
slash  = Literal("/")
bslash = Literal("\\")
star   = Literal("*")
semi   = Literal(";")
at     = Literal("@")
minus  = Literal("-")
pluss  = Literal("+")
quote = Literal('"')# | Literal("'")

#------------------------------------------------------------------------------
#  Compass point:
#------------------------------------------------------------------------------

north = CaselessLiteral("n")
northeast = CaselessLiteral("ne")
east = CaselessLiteral("e")
southeast = CaselessLiteral("se")
south = CaselessLiteral("s")
southwest = CaselessLiteral("sw")
west = CaselessLiteral("w")
northwest = CaselessLiteral("nw")
middle = CaselessLiteral("c")
underscore = CaselessLiteral("_")

compass_pt = (north | northeast | east | southeast | south | southwest |
    west | northwest | middle | underscore)

#------------------------------------------------------------------------------
#  Convenient pyparsing constructs.
#------------------------------------------------------------------------------

decimal_sep = "."

sign = oneOf("+ -")

scolon = Literal(";").suppress()

matlab_comment = Group(Literal('%') + restOfLine).suppress()
psse_comment = Literal('@!') + Optional(restOfLine)

# part of printables without decimal_sep, +, -
special_chars = string.replace(
    '!"#$%&\'()*,./:;<=>?@[\\]^_`{|}~', decimal_sep, ""
)

#------------------------------------------------------------------------------
#  "ToBoolean" class:
#------------------------------------------------------------------------------

class ToBoolean(TokenConverter):
    """ Converter to make token boolean """

    def postParse(self, instring, loc, tokenlist):
        """ Converts the first token to boolean """

        return bool(tokenlist[0])

#------------------------------------------------------------------------------
#  "ToInteger" class:
#------------------------------------------------------------------------------

class ToInteger(TokenConverter):
    """ Converter to make token into an integer """

    def postParse(self, instring, loc, tokenlist):
        """ Converts the first token to an integer """

        return int(tokenlist[0])

#------------------------------------------------------------------------------
#  "ToFloat" class:
#------------------------------------------------------------------------------

class ToFloat(TokenConverter):
    """ Converter to make token into a float """

    def postParse(self, instring, loc, tokenlist):
        """ Converts the first token into a float """

        return float(tokenlist[0])

#------------------------------------------------------------------------------
#  "ToTuple" class:
#------------------------------------------------------------------------------

class ToTuple(TokenConverter):
    """ Converter to make token sequence into a tuple. """

    def postParse(self, instring, loc, tokenlist):
        """ Returns a tuple initialised from the token sequence. """

        return tuple(tokenlist)

#------------------------------------------------------------------------------
#  "ToList" class:
#------------------------------------------------------------------------------

class ToList(TokenConverter):
    """ Converter to make token sequence into a list. """

    def postParse(self, instring, loc, tokenlist):
        """ Returns a list initialised from the token sequence. """

        return list(tokenlist)

# Integer ---------------------------------------------------------------------

integer = ToInteger(
    Optional(quote).suppress() +
    Combine(Optional(sign) + Word(nums)) +
    Optional(quote).suppress()
).setName("integer")

positive_integer = ToInteger(
    Combine(Optional("+") + Word(nums))
).setName("integer")

negative_integer = ToInteger(
    Combine("-" + Word(nums))
).setName("integer")

# Boolean ---------------------------------------------------------------------

#boolean = ToBoolean(ToInteger(Word("01", exact=1))).setName("bool")
true = CaselessLiteral("True") | Literal("1") #And(integer, NotAny(Literal("0")))
false = CaselessLiteral("False") | Literal("0")
boolean = ToBoolean(true | false).setResultsName("boolean")

# Real ------------------------------------------------------------------------

real = ToFloat(
    Optional(quote).suppress() +
    Combine(
        Optional(sign) +
        (Word(nums) + Optional(decimal_sep + Word(nums))) |
        (decimal_sep + Word(nums)) +
        Optional(oneOf("E e") + Word(nums))
    ) +
    Optional(quote).suppress()
).setName("real")

# TODO: Positive real number between zero and one.
decimal = real

# String ----------------------------------------------------------------------

q_string = (sglQuotedString | dblQuotedString).setName("q_string")

#double_quoted_string = QuotedString('"', multiline=True,escChar="\\",
#    unquoteResults=True) # dblQuotedString
double_quoted_string = Regex(r'\"(?:\\\"|\\\\|[^"])*\"', re.MULTILINE)
double_quoted_string.setParseAction(removeQuotes)
quoted_string = Combine(
    double_quoted_string+
    Optional(OneOrMore(pluss+double_quoted_string)), adjacent=False
)
word = quoted_string.setName("word") # Word(alphanums)

# Graph attributes ------------------------------------------------------------

hex_color = Word(hexnums, exact=2) #TODO: Optional whitespace
rgb = Literal("#").suppress() + hex_color.setResultsName("red") + \
    hex_color.setResultsName("green") + hex_color.setResultsName("blue")
rgba = rgb + hex_color.setResultsName("alpha")
hsv = decimal.setResultsName("hue") + decimal.setResultsName("saturation") + \
    decimal.setResultsName("value")
color_name = double_quoted_string | Word(alphas)
colour = rgba | rgb | hsv | color_name

#------------------------------------------------------------------------------
#  A convenient function for calculating a unique name given a list of
#  existing names.
#------------------------------------------------------------------------------

def make_unique_name(base, existing=[], format="%s_%s"):
    """
    Return a name, unique within a context, based on the specified name.

    base: the desired base name of the generated unique name.
    existing: a sequence of the existing names to avoid returning.
    format: a formatting specification for how the name is made unique.

    """

    count = 2
    name = base
    while name in existing:
        name = format % (base, count)
        count += 1

    return name

#------------------------------------------------------------------------------
#  "nsplit" function:
#------------------------------------------------------------------------------

def nsplit(seq, n=2):
    """ Split a sequence into pieces of length n

    If the length of the sequence isn't a multiple of n, the rest is discarded.
    Note that nsplit will split strings into individual characters.

    Examples:
    >>> nsplit("aabbcc")
    [("a", "a"), ("b", "b"), ("c", "c")]
    >>> nsplit("aabbcc",n=3)
    [("a", "a", "b"), ("b", "c", "c")]

    # Note that cc is discarded
    >>> nsplit("aabbcc",n=4)
    [("a", "a", "b", "b")]

    """

    return [xy for xy in itertools.izip(*[iter(seq)]*n)]

#------------------------------------------------------------------------------
#  "windows" function:
#------------------------------------------------------------------------------

def windows(iterable, length=2, overlap=0, padding=True):
    """ Code snippet from Python Cookbook, 2nd Edition by David Ascher,
    Alex Martelli and Anna Ravenscroft; O'Reilly 2005

    Problem: You have an iterable s and need to make another iterable whose
    items are sublists (i.e., sliding windows), each of the same given length,
    over s' items, with successive windows overlapping by a specified amount.

    """

    it = iter(iterable)
    results = list(itertools.islice(it, length))
    while len(results) == length:
        yield results
        results = results[length-overlap:]
        results.extend(itertools.islice(it, length-overlap))
    if padding and results:
        results.extend(itertools.repeat(None, length-len(results)))
        yield results


if __name__ == "__main__":
    l = [1,2,3,4]
    for j, k in windows(l, length=2, overlap=1, padding=False):
        print j, k
    print nsplit(l)

# EOF -------------------------------------------------------------------------

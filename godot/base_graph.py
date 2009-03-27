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

""" Defines a base class for many graphs. """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import os

import tempfile

from enthought.traits.api \
    import HasTraits, Str, List, Instance, Bool, Property, Constant, \
    ReadOnly, Dict, TraitListEvent, Int, Enum, on_trait_change

from enthought.enable.api \
    import Viewport, Container

from enthought.enable.tools.api \
    import ViewportPanTool, ViewportZoomTool

from node \
    import Node

from edge \
    import Edge

from common \
    import id_trait, Alias

import godot

#from util import Serializable

FORMATS = ['dot', 'canon', 'cmap', 'cmapx', 'cmapx_np', 'dia', 'fig', 'gd',
           'gd2', 'gif', 'hpgl', 'imap', 'imap_np', 'ismap', 'jpe', 'jpeg',
           'jpg', 'mif', 'mp', 'pcl', 'pdf', 'pic', 'plain', 'plain-ext',
           'png', 'ps', 'ps2', 'svg', 'svgz', 'vml', 'vmlz', 'vrml', 'vtx',
           'wbmp', 'xdot', 'xlib', 'bmp', 'eps', 'gtk', 'ico', 'tga', 'tiff']

RENDERERS = ['cairo', 'gd']

FORMATTERS = ['cairo', 'gd', 'gdk_pixbuf']

#------------------------------------------------------------------------------
#  "BaseGraph" class:
#------------------------------------------------------------------------------

class BaseGraph ( HasTraits ):
    """ Defines a representation of a graph in Graphviz's dot language """

    #--------------------------------------------------------------------------
    #  Trait definitions.
    #--------------------------------------------------------------------------

    # Optional unique identifier.
    ID = id_trait

    # Synonym for ID.
    name = Alias("ID", desc="synonym for ID") # Used by InstanceEditor

    # Main graph nodes.
    nodes = List( Instance(Node) )

    # Map if node IDs to node objects.
#    id_node_map = Dict

    # Graph edges.
    edges = List(Instance(Edge))

    # Separate layout regions.
    subgraphs = List(Instance("godot.subgraph.Subgraph"))

    # Clusters are encoded as subgraphs whose names have the prefix 'cluster'.
    clusters = List(Instance("godot.cluster.Cluster"))

    # Node from which new nodes are cloned.
    default_node = Instance(Node)

    # Edge from which new edges are cloned.
    default_edge = Instance(Edge)

    # Graph from which new subgraphs are cloned.
    default_graph = Instance(HasTraits)

    # Level of the graph in the subgraph hierarchy.
#    level = Int(0, desc="level in the subgraph hierarchy")

    # Padding to use for pretty string output.
    padding = Str("    ", desc="padding for pretty printing")

    # A dictionary containing the Graphviz executable names as keys
    # and their paths as values.  See the trait initialiser.
    programs = Dict(desc="names and paths of Graphviz executables")

    # The Graphviz layout program
    program = Enum("dot", "circo", "neato", "twopi", "fdp",
        desc="layout program used by Graphviz")

    # Format for writing to file.
    format = Enum(FORMATS, desc="format used when writing to file")

    #--------------------------------------------------------------------------
    #  Enable trait definitions.
    #--------------------------------------------------------------------------

    # Container of graph components.
    component = Instance(Container, desc="container of graph components.")

    # A view into a sub-region of the canvas.
    vp = Instance(Viewport, desc="a view of a sub-region of the canvas")

    #--------------------------------------------------------------------------
    #  Xdot trait definitions:
    #--------------------------------------------------------------------------

    # For a given graph object, one will typically a draw directive before the
    # label directive. For example, for a node, one would first use the
    # commands in _draw_ followed by the commands in _ldraw_.
    _draw_ = Str(desc="xdot drawing directive")

    # Label draw directive.
    _ldraw_ = Str(desc="xdot label drawing directive")

    #--------------------------------------------------------------------------
    #  "object" interface:
    #--------------------------------------------------------------------------

#    def __init__(self, **traits):
#        """ Initialises a new BaseGraph instance.
#        """
#        super(BaseGraph, self).__init__(**traits)
#
#        # Automatically creates all the methods enabling the saving
#        # of output in any of the supported formats.
#        for frmt in FORMATS:
#            self.__setattr__('save_'+frmt,
#                             lambda flo, f=frmt, prog=self.program: \
#                             flo.write( self.create(format=f, prog=prog) ))
#            f = self.__dict__['save_'+frmt]
#            f.__doc__ = '''Refer to the docstring accompanying the 'create'
#            method for more information.'''


    def __len__(self):
        """ Return the order of the graph when requested by len().

            @rtype:  number
            @return: Size of the graph.
        """
        return len(self.nodes)


    def __iter__(self):
        """ Return a iterator passing through all nodes in the graph.

            @rtype:  iterator
            @return: Iterator passing through all nodes in the graph.
        """
        for each in self.nodes:
            yield each


    def __getitem__(self, node):
        """ Return a iterator passing through all neighbours of the given node.

            @rtype:  iterator
            @return: Iterator passing through all neighbours of the given node.
        """
        for each_edge in self.edges:
            if (each_edge.tail_node == node) or (each_edge.head_node == node):
                yield each_edge


    def __str__(self):
        """ Returns a string representation of the graph in dot language. It
            will return the graph and all its subelements in string form.
        """
        s = ""
        padding = self.padding
        if self.ID:
            s += "%s {\n" % self.ID
        else:
            s += "{\n"

        # Traits to be included in string output have 'graphviz' metadata.
        for trait_name, trait in self.traits(graphviz=True).iteritems():
            # Get the value of the trait for comparison with the default.
            value = getattr(self, trait_name)

            # Only print attribute value pairs if not defaulted.
            # FIXME: Alias/Synced traits default to None.
            if ( value != trait.default ) and ( trait.default is not None ):
                if isinstance( value, basestring ):
                    # Add double quotes to the value if it is a string.
                    valstr = '"%s"' % value
                else:
                    valstr = str(value)

                s += "%s%s=%s;\n" % ( padding, trait_name, valstr )

        def prepend_padding(s):
            return "\n".join( [padding + line for line in s.splitlines()] )

        for node in self.nodes:
            s += "%s%s\n" % ( padding, str(node) )
        for edge in self.edges:
            s += "%s%s\n" % ( padding, str(edge) )
        for subgraph in self.subgraphs:
            s += prepend_padding( str( subgraph ) ) + "\n"
        for cluster in self.clusters:
            s += prepend_padding( str( cluster ) ) + "\n"

        s += "}"

        return s

    #--------------------------------------------------------------------------
    #  Trait initialisers:
    #--------------------------------------------------------------------------

    def _default_node_default(self):
        """ Trait initialiser.
        """
        return Node("default")


    def _default_edge_default(self):
        """ Trait initialiser.
        """
        return Edge("tail", "head")


    def _default_graph_default(self):
        """ Trait initialiser.
        """
        return godot.cluster.Cluster(ID="cluster_default")


    def _component_default(self):
        """ Trait initialiser.
        """
        return Container(fit_window=False, auto_size=True)


    def _vp_default(self):
        """ Trait initialiser.
        """
        vp = Viewport(component=self.component)
        vp.enable_zoom=True

        vp.view_position = [0,0]

        vp.tools.append(ViewportPanTool(vp))

        return vp

    #--------------------------------------------------------------------------
    #  Public interface:
    #--------------------------------------------------------------------------

    def save_dot(self, flo, prog=None):
        """ Writes a graph to a file.

            Given a file like object 'flo' it will truncate it and write a
            representation of the graph defined by the dot object and in the
            format specified.
            The format 'raw' is used to dump the string representation
            of the Dot object, without further processing.
            The output can be processed by any of graphviz tools, defined
            in 'prog', which defaults to 'dot'.
        """
        flo.write( str(self) )


    def save_xdot(self, flo, prog=None):
        prog = self.program if prog is None else prog
        flo.write( self.create(prog, "xdot") )


    def save_png(self, flo, prog=None):
        prog = self.program if prog is None else prog
        flo.write( self.create(prog, "png") )


    @classmethod
    def load_dot(cls, flo):
        parser = godot.dot_data_parser.GodotDataParser()
        return parser.parse_dot_file(flo)


    @classmethod
    def load_xdot(cls, flo):
        parser = godot.dot_data_parser.GodotDataParser()
        return parser.parse_dot_file(flo)


    def create(self, prog=None, format=None):
        """ Creates and returns a representation of the graph using the
            Graphviz layout program given by 'prog', according to the given
            format.

            Writes the graph to a temporary dot file and processes it with
            the program given by 'prog' (which defaults to 'dot'), reading
            the output and returning it as a string if the operation is
            successful. On failure None is returned.
        """
        prog = self.program if prog is None else prog
        format = self.format if format is None else format

        # Make a temporary file ...
        tmp_fd, tmp_name = tempfile.mkstemp()
        os.close( tmp_fd )
        # ... and save the graph to it.
        self.save_to_file(tmp_name, format="dot")

        # Get the temporary file directory name.
        tmp_dir = os.path.dirname( tmp_name )

        # TODO: Shape image files (See Pydot).

        # Process the file using the layout program, specifying the format.
        p = subprocess.Popen(
            ( self.programs[ prog ], '-T'+format, tmp_name ),
            cwd=tmp_dir,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        stderr = p.stderr
        stdout = p.stdout

        # Make sense of the standard output form the process.
        stdout_output = list()
        while True:
            data = stdout.read()
            if not data:
                break
            stdout_output.append(data)
        stdout.close()

        if stdout_output:
            stdout_output = ''.join(stdout_output)

        # Similarly so for any standard error.
        if not stderr.closed:
            stderr_output = list()
            while True:
                data = stderr.read()
                if not data:
                    break
                stderr_output.append(data)
            stderr.close()

            if stderr_output:
                stderr_output = ''.join(stderr_output)

        #pid, status = os.waitpid(p.pid, 0)
        status = p.wait()

        if status != 0 :
            logger.error("Program terminated with status: %d. stderr " \
                "follows: %s" % ( status, stderr_output ) )
        elif stderr_output:
            logger.error( "%s", stderr_output )

        # TODO: Remove shape image files from the temporary directory.

        # Remove the temporary file.
        os.unlink(tmp_name)

        return stdout_output


    def arrange_all(self):
        """ Sets for the _draw_ and _ldraw_ attributes for each of the graph
            sub-elements by processing the xdot format of the graph.
        """
        xdot_data = self.create( format = "xdot" )

        print "XDOT DATA:\n\n", xdot_data

        parser = dot_parser.DotParser()
        xdot_graph = parser.parse_dot_data( xdot_data )


    def add_node(self, node_or_ID, **kwds):
        """ Adds a node to the graph.
        """
        if not isinstance(node_or_ID, Node):
            nodeID = str( node_or_ID )
            if nodeID in self.nodes:
                node = self.nodes[ self.nodes.index(nodeID) ]
            else:
                if self.default_node is not None:
                    node = self.default_node.clone_traits(copy="deep")
                    node.ID = nodeID
                else:
                    node = Node(nodeID)
                self.nodes.append( node )
        else:
            node = node_or_ID
            if node in self.nodes:
                node = self.nodes[ self.nodes.index(node_or_ID) ]
            else:
                self.nodes.append( node )

        node.set( **kwds )

        return node


    def delete_node(self, node_or_ID):
        """ Removes a node from the graph.
        """
        if isinstance(node_or_ID, Node):
            name = node.ID
        else:
            name = node_or_ID

        self.nodes = [n for n in self.nodes if n.ID != name]


    def get_node(self, ID):
        """ Returns the node with the given ID or None.
        """
        for node in self.nodes:
            if node.ID == ID:
                return node
        else:
            return None


    def add_edge(self, tail_node_or_ID, head_node_or_ID, **kwds):
        """ Adds an edge to the graph.
        """
        tail_node = self.add_node(tail_node_or_ID)
        head_node = self.add_node(head_node_or_ID)

        # Only top level graphs are directed and/or strict.
        if "directed" in self.trait_names():
            directed = self.directed
        else:
            directed = False

        if self.default_edge is not None:
            edge = self.default_edge.clone_traits(copy="deep")
            edge.set( **kwds )
        else:
            edge = Edge(tail_node, head_node, directed, **kwds)

        if "strict" in self.trait_names():
            if not self.strict:
                self.edges.append(edge)
            else:
                raise NotImplementedError
        else:
            self.edges.append(edge)


    def add_subgraph(self, subgraph_or_ID):
        """ Adds a subgraph to the graph.
        """
        if not isinstance(subgraph_or_ID, (godot.subgraph.Subgraph,
                                           godot.cluster.Cluster)):
            subgraphID = str( subgraph_or_ID )
            if subgraph_or_ID.startswith("cluster"):
                subgraph = godot.cluster.Cluster(ID=subgraphID)
            else:
                subgraph = godot.subgraph.Subgraph(ID=subgraphID)
        else:
            subgraph = subgraph_or_ID

        subgraph.default_node = self.default_node
        subgraph.default_edge = self.default_edge
#        subgraph.level = self.level + 1
#        subgraph.padding += self.padding

        if isinstance(subgraph, godot.subgraph.Subgraph):
            self.subgraphs.append(subgraph)
        elif isinstance(subgraph, godot.cluster.Cluster):
            self.clusters.append(subgraph)
        else:
            raise

        return subgraph


    def add_cluster(self, cluster_or_ID):
        """ Adds a cluster to the graph.
        """
        return self.add_subgraph(cluster_or_ID)

    #--------------------------------------------------------------------------
    #  "BaseGraph" interface:
    #--------------------------------------------------------------------------

#    @on_trait_change("nodes,nodes_items")
#    def remove_duplicates(self, new):
#        """ Ensures node ID uniqueness.
#        """
#        if isinstance(new, TraitListEvent):
#            old = event.removed
#            new = event.added
#
#        set = {}
#        self.set( trait_change_notify = False,
#                  nodes = [set.setdefault(e, e) for e in new if e not in set] )


    @on_trait_change("nodes,nodes_items")
    def _set_node_lists(self, new):
        """ Maintains each edge's list of available nodes.
        """
        for edge in self.edges:
            edge._nodes = self.nodes


#    @on_trait_change("nodes,nodes_items")
#    def _manage_id_node_map(self, obj, name, old, new):
#        """ Maintains a dictionary mapping node IDs to nodes.
#        """
#        if isinstance(new, TraitListEvent):
#            old = event.removed
#            new = event.added
#        else:
#            self.id_node_map = {}
#
#        for new_node in new:
#            self.id_node_map[new_node.ID] = new_node
#
#        for old_node in old:
#            try:
#                self.id_node_map.pop(node.ID)
#            except KeyError:
#                print "Removed node not found in ID map. Updating."
#                self._update_id_node_map()


    def _nodes_items_changed(self, event):
        """ Handles addition and removal of nodes.
        """
        # Add new nodes to the canvas.
        from enthought.enable.primitives.api import Box
        from enthought.enable.tools.api import MoveTool

        for node in event.added:
            box = Box(color="steelblue", border_color="darkorchid",
                border_size=1, bounds=[50, 50], position=[10, 10])
            box.tools.append(MoveTool(box))
            self.component.add(box)
            self.component.add(node.component)

        self.component.request_redraw()


#    def _update_id_node_map(self):
#        """ Sets the map of node IDs to nodes.
#        """
#        d = {}
#        for node in self.nodes:
#            d[node.ID] = node
#        self.id_node_map = d

# EOF -------------------------------------------------------------------------

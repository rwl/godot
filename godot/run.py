""" Godot application entry point.
"""
import logging

from enthought.envisage.core_plugin import CorePlugin

from envisage.plugin import EnvisagePlugin
from envisage.resource.resource_plugin import ResourcePlugin
from envisage.workbench.workbench_plugin import WorkbenchPlugin
from envisage.workbench.workbench_application import WorkbenchApplication

from enthought.pyface.api import ImageResource

from godot.plugin.godot_plugin import GodotPlugin

logger = logging.getLogger()
logger.addHandler( logging.StreamHandler() )
logger.setLevel(logging.DEBUG)

class GodotApplication(WorkbenchApplication):
    id = "com.github.pylon"
    icon = ImageResource("dot.ico", search_path=["ui"])
    name = "Godot"

def main():
    """ Runs Godot.
    """
    application = GodotApplication( id="godot",
        plugins=[CorePlugin(),
                 EnvisagePlugin(),
                 WorkbenchPlugin(),
                 ResourcePlugin(),
                 GodotPlugin()] )

    application.run()

if __name__ == "__main__":
    main()

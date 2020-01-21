from xicam.plugins import GUILayout, GUIPlugin
from xicam.gui.widgets.imageviewmixins import CatalogView, BetterButtons
from qtpy.QtWidgets import QLabel

# not explicitly needed, could be useful for type hint
from databroker.core import BlueskyRun

# Create a blend of class from 2 xicam image view mixins
class MyImageViewer(BetterButtons, CatalogView):
    def __init__(self, *args, **kwargs):
        super(MyImageViewer, self).__init__(*args, **kwargs)


class MyGUIPlugin(GUIPlugin):
    # defines name for plugin for display in xi-cam
    name = 'My Plugin'  
    def __init__(self):

        # Define stages
        # GUILayout must provide a center widget
        # self.catalog_view = CatalogView() # QLabel('hello')
        
        # instead using MyImageViewer.  Adds different buttons to catalogview
        self.catalog_view = MyImageViewer()

        lefttop_widget = QLabel('lefttop')
        stage_layout = GUILayout(lefttop=lefttop_widget, center=self.catalog_view)
        # self.stages defines GUILayouts
        # self.stages is a dictionary contianing:
        #       stage name -> GUILayout
        #       stage name 2 -> GUILayout 2
        #       ...
        self.stages = { 
            'first stage': stage_layout 
        }

        # newer suggested format for super()
        # here need to run super after GUILayouts
        super(MyGUIPlugin, self).__init__()

    # Overrides GUIPlugin's method
    # Tells xicam what to do when catalog is opened under this plugin
    # eg in CatalogViewer, it was a qtGraphViewer
    def appendCatalog(self, catalog:BlueskyRun):
        # catalog:BlueskyRun hints at type, but does not enforce
        """
        Inuts:
            catalog: BlueskyRun
        """

        # hard codes primary stream, img stream
        # different methods for defining watched streams exist

        # need this line to tell xicam what to do with catalog.
        # here, opening a file displays it to the catalog_view
        self.catalog_view.setCatalog(catalog, 'primary', 'img')
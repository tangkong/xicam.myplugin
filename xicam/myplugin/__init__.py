from xicam.plugins import GUILayout, GUIPlugin
from xicam.gui.widgets.imageviewmixins import CatalogView, BetterButtons
from qtpy.QtWidgets import (QLabel, QHBoxLayout, QWidget, QPushButton, 
                        QMessageBox, QVBoxLayout)
from xicam.core.msg import notifyMessage

# not explicitly needed, could be useful for type hint
from databroker.core import BlueskyRun

# Import workflow stuff (from operationplugin branch)
from .workflows import MyWorkflow

# Create a blend of class from 2 xicam image view mixins
class MyImageViewer(BetterButtons, CatalogView):
    def __init__(self, *args, **kwargs):
        super(MyImageViewer, self).__init__(*args, **kwargs)


class MyGUIPlugin(GUIPlugin):
    # defines name for plugin for display in xi-cam
    name = 'My Plugin'  
    def __init__(self):
        # Define workflows
        self.my_workflow = MyWorkflow()
        
        # Define stages
        # GUILayout must provide a center widget
        
        # # 1: Basic center catalog view widget
        # self.catalog_view = CatalogView() # QLabel('hello')
        
        # # 2: instead using MyImageViewer.  Adds different buttons to catalogview
        # self.catalog_view = MyImageViewer()
        # stage_layout = GUILayout(lefttop=lefttop_widget, 
        #                       center=self.catalog_view)

        # 3: more complicated center widget
        center_widget = QWidget() # center widget base
        layout = QVBoxLayout() # Inialize horizontal layout
        self.catalog_view = MyImageViewer()
        self.label = QLabel("1")
        layout.addWidget(self.catalog_view)  # Add first Horiz widget to layout
        layout.addWidget(self.label) # Add second Horiz widget layout
        # 4: adding buttons etc 
        self.button = QPushButton("Button")
        layout.addWidget(self.button)
        # (3,4) initializing center widget
        center_widget.setLayout(layout)
        # Must pass a widget to GUILayout.  Widgets have layouts though
        stage_layout = GUILayout(center=center_widget) 

        # Define some connections
        # SYNTAX: variable.<SIGNAL>.connect(<SLOT>:function)
        # SIGNALs are emitted when a gui "event" happens (click, change, etc)
        # Different QObjects define/emit different SIGNALs
        # Connect a SIGNAL to a function (called SLOT)
        #   function/SLOT called when SIGNAL emitted (event happens)
        self.button.clicked.connect(self.update_label)
        self.button.clicked.connect(self.show_message)
        self.button.clicked.connect(self.run_workflow)
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

    # Slots for connections to signals ---------------------------------------
    def update_label(self):
        """ <SLOT> Method to pass into connection """ 
        current_text = self.label.text()
        current_text += "1"
        self.label.setText(current_text)

    def show_message(self):
        """ <SLOT> """
        # self designates what widget to show above
        notifyMessage('Add Another 1.')

    def show_message(self, catalog:BlueskyRun):
        """ <SLOT> """
        notifyMessage('print catalog: {}'.format(catalog))

    def run_workflow(self):
        """ 
        <SLOT> run our workflow 
        Workflow class has an exec() and exec() all to run itself
        """
        # extract data from loaded catalog (assumes button is enabled)
        if not self.catalog_view.catalog:
            notifyMessage('No catalog loaded, please open one')
            return 
            
        # primary and 'img' should not be hard coded here
        # # to_dask gives lazy objects
        # image_data = self.catalog_view.catalog.primary.to_dask['img'].compute
        image_data = self.catalog_view.catalog.primary.read()['img']
        # can pass in input data, and function to call when it's done
        self.my_workflow.execute(input_image=image_data, 
                                callback_slot=self.show_fft)

    # Workflow callback_slot's have *results passed into them
    # results: a list of result objects
    # eg: [{'output_image': np.ndarray}]
    def show_fft(self, *results):
        fft_image = results[-1]['output_image']
        import matplotlib.pyplot as plt
        plt.imshow(fft_image[0])
        plt.show()

    #-------------------------------------------------------------------------
    
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
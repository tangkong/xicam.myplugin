# Import workflow stuff (from operationplugin branch)
from xicam.core.execution import Workflow
from xicam.plugins.operationplugin import OperationPlugin

from ..operations import fft

class MyWorkflow(Workflow):
    def __init__(self):
        super(MyWorkflow, self).__init__()
        
        self.add_operation(fft)
        # can add other operations 

        self.auto_connect_all()
import numpy as np
from xicam.plugins.operationplugin import OperationPlugin, output_names

# How to define an operation plugin...
# define a python function with type hinting
# then add special decorators

# inputs are defined as function parameters
# outputs are defined using a decorator, output_names

# turn function into operation plugin with decorator
@OperationPlugin
@output_names("output_image")
def fft(input_image:np.ndarray=[0]) -> np.ndarray:
    output = np.absolute(np.fft.fftn(input_image))
    return output
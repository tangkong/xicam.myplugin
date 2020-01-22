import numpy as np

#from scipy.spatial import distance
from xicam.plugins.operationplugin import OperationPlugin, output_names

# How to define an operation plugin...
# define a python function with type hinting
# then add special decorators

# inputs are defined as function parameters
# outputs are defined using a decorator, output_names

# turn function into operation plugin with decorator
@OperationPlugin
@output_names("output_image")
def fft(input_image:np.ndarray=np.zeros(1,)) -> np.ndarray:
    output = np.absolute(np.fft.fftshift(np.fft.fft2(input_image)))
    return output


# @OperationPlugin
# @output_names("output_image_fftn")
# def fftn(input_image:np.ndarray=[0]) -> np.ndarray:
#     output = np.absolute(np.fft.fftshift(np.fft.fftn(input_image)))
#     return output

# @OperationPlugin
# @output_names("output_image_threshold")
# def threshold(input_image:np.ndarray=np.zeros(5,)) -> np.ndarray:
#     low = 0.1
#     im_min = input_image.min()
#     im_max = input_image.max()
#     low_bound = im.min + low*distance.euclidian(im_min, im_max)
#     high = 0.9
#     high_bound = im_max + high * distance.euclidian(im_min, im_max)

#     output = input_image
#     output[(output < low_bound)] = 0
#     output[(output > high_bound)] = 0
#     return output
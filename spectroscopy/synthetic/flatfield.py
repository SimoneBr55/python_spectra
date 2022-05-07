import numpy as np

from spectroscopy.convenience_functions import show_image
from spectroscopy.synthetic.sky_background import *
from spectroscopy.synthetic.biasframe import *
from spectroscopy.synthetic.darkframe import *
from spectroscopy.synthetic.image_defects import *

def flat(image=np.zeros([2000,2000]), show=False, title="Flat Field"):
    """
    Generate a flat field
    :param image: numpy array, optional [image whose shape to match]
    :param show: bool, optional
    :param title: string, optional
    :return:
    """
    flat = sensitivity_variations(image, show=show)

    return flat
import os

# %matplotlib inline # only in jupiter notebook

from matplotlib import pyplot as plt
import numpy as np
from photutils.aperture import EllipticalAperture
from spectroscopy.convenience_functions import show_image
"""Boiler Plate Code"""
plt.style.use('files/guide.mplstyle')  # custom style from the guide (fonts and figures)
# Random Generator
seed = os.getenv('GUIDE_RANDOM_SEED', None)
if seed is not None:
    seed = int(seed)
# generate Poisson error to simulate random noise
noise_rng = np.random.default_rng(seed)
""""""

def dark_current(image, current, exposure_time, gain=1.0, hot_pixels=False, show=False, title="Dark Current"):
    """
    Simulate dark current in a CCD, optionally with hot pixels.

    :param image: numpy array [image whose shape to match]
    :param current: float [electrons/pixels/second]
    :param exposure_time: float [length of the simulated exposure in seconds]
    :param gain: float, optional [electrons/ADU]
    :param hot_pixels: float, optional [cosmic rays / hot pixels count]
    :return: numpy array [image]
    """
    # dark current for every pixel
    base_current = current * exposure_time / gain

    dark_im = noise_rng.poisson(base_current, size=image.shape)

    if hot_pixels:
        y_max, x_max = dark_im.shape
        #  We will set 0.01% of pixels to be hot. Too high but at least they become visible
        n_hot = int(0.0001 * x_max * y_max)

        # We want hot pixels to always be in the same places, but they have to be randomly distributed.
        rng = np.random.RandomState(16201649)
        hot_x = rng.randint(0, x_max, size=n_hot)
        hot_y = rng.randint(0, y_max, size=n_hot)

        hot_current = 10000 * current
        dark_im[(hot_y, hot_x)] = hot_current * exposure_time / gain

    if show:
        show_image(dark_im, cmap='gray', title=title)
    return dark_im

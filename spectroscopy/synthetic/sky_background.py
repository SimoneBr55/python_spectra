import os

# %matplotlib inline # only in jupiter notebook

from matplotlib import pyplot as plt
import numpy as np
from photutils.aperture import EllipticalAperture
from spectroscopy.convenience_functions import show_image

from photutils.datasets import make_random_gaussians_table, make_gaussian_sources_image
"""Boiler Plate Code"""
plt.style.use('~/GitHub/python_spectra/files/guide.mplstyle')  # custom style from the guide (fonts and figures)
# Random Generator
seed = os.getenv('GUIDE_RANDOM_SEED', None)
if seed is not None:
    seed = int(seed)
# generate Poisson error to simulate random noise
noise_rng = np.random.default_rng(seed)
""""""

def sky_background(image, sky_counts, gain=1, show=False, title='Sky Background'):
    """
    Generate sky background.

    :param image: numpy array [image whose shape to match]
    :param sky_counts: float [counts from the sky]
    :param gain: float, optional [electrons/ADU]
    :return: numpy array [image]
    """
    sky_im = noise_rng.poisson(sky_counts * gain, size=image.shape) / gain
    if show:
        show_image(sky_im, cmap='gray', title=title)
    return sky_im

def stars(image, number, max_counts=10000, gain=1, fwhm=4, show=False, title="Star Field"):
    """
    Add some stars to an image
    :param image: numpy array [image to start from]
    :param number: int [number of stars]
    :param max_counts: float, optional [number of counts per star]
    :param gain: float, optional [electrons/ADU]
    :param fwhm: float, optional [size of stars]
    :param show: bool, optional [show the image or not]
    :param title: string, optional [title of frame]
    :return: numpy array [image]
    """
    flux_range = [max_counts / 10, max_counts]

    y_max, x_max = image.shape
    xmean_range = [0.1 * x_max, 0.9 * x_max]
    ymean_range = [0.1 * y_max, 0.9 * y_max]

    xstddev_range = [fwhm, fwhm]
    ystddev_range = [fwhm, fwhm]
    params = dict([('amplitude', flux_range),
                   ('x_mean', xmean_range),
                   ('y_mean', ymean_range),
                   ('x_stddev', xstddev_range),
                   ('y_stddev', ystddev_range),
                   ('theta', [0,2 * np.pi])])
    sources = make_random_gaussians_table(number, params, seed=12345)
    star_im = make_gaussian_sources_image(image.shape, sources)
    if show:
        show_image(star_im, cmap='gray', percu=99.9, title=title)

    return star_im
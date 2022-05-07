import os
import numpy as np
from photutils.aperture import EllipticalAperture
from spectroscopy.convenience_functions import show_image
from astropy.modeling.models import Gaussian2D, RickerWavelet2D, Const2D


seed = os.getenv('GUIDE_RANDOM_SEED', None)
default_rng = np.random.default_rng(seed)
if seed is not None:
    seed = int(seed)



def make_cosmic_rays(image, number, strength=10000, show=False, title="Cosmic Rays"):
    """
    Generate an image with some cosmic rays

    :param image: numpy array [image whose shape to match]
    :param number: float [number of cr to add]
    :param strength: float, optional [pixel count in the cosmic rays
    :param show: bool, optional
    :param title: string, optional
    :return: numpy array [image]
    """
    cr_image = np.zeros_like(image)

    max_y, max_x = cr_image.shape

    # Ensure that the cosmic rays are within the image
    maximum_pos = np.min(cr_image.shape)

    # Define the center points for the CRs, away from the edges
    xy_cr = default_rng.integers(0.1 * maximum_pos, 0.9 * maximum_pos, size=[number, 2])

    cr_length = 5  # pixels
    cr_width = 2
    theta_cr = 2 * np.pi  *default_rng.uniform()
    apertures = EllipticalAperture(xy_cr, cr_length, cr_width, theta_cr)
    masks = apertures.to_mask(method='center')

    for mask in masks:
        cr_image += strength * mask.to_image(shape=cr_image.shape)

    if show:
        show_image(cr_image, cmap='gray', title=title)
    return cr_image

def make_one_donut(center, diameter=10, amplitude=0.25):
    """
    Make one grain of dust on the sensor
    :param center: float [center position of grain]
    :param diameter: float [diameter of donut]
    :param amplitude: float [amplitude of gaussian]
    :return: CompoundModel
    """
    sigma = diameter / 2
    mh = RickerWavelet2D(amplitude=amplitude, x_0=center[0], y_0=center[1], sigma=sigma)
    gauss = Gaussian2D(amplitude=amplitude, x_mean=center[0], y_mean=center[1], x_stddev=sigma, y_stddev=sigma)

    donut = Const2D(amplitude=1) + (mh -gauss)

    return donut

def add_donuts(image, number=20, show=False, title="Grains of Sand"):
    """
    Generate a matrix by which you multiply input counts to obtain actual counts.

    :param image: numpy array [image whose shape to match]
    :param number: int, optional [number of dust donuts]
    :param show: bool, optional
    :param title: string, optional
    :return: numpy array [transfer function matrix]
    """

    y, x = np.indices(image.shape)

    # Dust always in the same places
    rng = np.random.RandomState(43901)
    shape = np.array(image.shape)
    border_padding = 50

    # Dust specks from 1% to 5% of the image size, but only in a couple of sizes.

    min_diam = int(0.02 * shape.max())
    max_diam = int(0.05 * shape.max())

    # Prefer smaller donuts to make it more realistic
    diameters = rng.choice([min_diam, min_diam, min_diam, max_diam], size=number)

    # Add a little variation
    amplitudes = rng.normal(0.25, 0.05, size=number)
    center_x = rng.randint(border_padding, high=shape[1] - border_padding, size=number)
    center_y = rng.randint(border_padding, high=shape[0] - border_padding, size=number)

    centers = [[x, y] for x, y in zip(center_x, center_y)]

    donut_model = make_one_donut(centers[0], diameter=diameters[0], amplitude=amplitudes[0])

    donut_im = donut_model(x,y)
    idx = 1
    for center, diam, amplitude in zip(centers[1:], diameters[1:], amplitudes[1:]):
        idx += 1
        donut_model = make_one_donut(center, diameter=diam, amplitude=amplitude)
        donut_im += donut_model(x,y)
    donut_im /= number

    if show:
        show_image(donut_im, cmap='gray', title=title)

    return donut_im

def sensitivity_variations(image, vignetting=True, dust=True, show=False, title='Sensitivity Variations'):
    """
    Matrix by which multiply input to get sensitivity variations
    :param image: numpy array [image whose shape to match]
    :param vignetting: bool, optional [show vignetting]
    :param dust: bool, optional [add dust]
    :return: numpy arrays [sensitivity variation transfer function]
    """

    sensitivity = np.zeros_like(image) + 1.0
    shape = np.array(sensitivity.shape)
    if dust or vignetting:
        y, x = np.indices(sensitivity.shape)

    if vignetting:
        vign_model = Gaussian2D(amplitude=1, x_mean=shape[0] / 2, y_mean=shape[1] / 2,
                                x_stddev=2 * shape.max(), y_stddev=2 * shape.max())
        # Very wide gaussian centered on the center of the image, and multiply by sensitivity.
        vign_im = vign_model(x, y)
        sensitivity *= vign_im

    if dust:
        dust_im = add_donuts(image, number=40)
        dust_im = dust_im / dust_im.max()
        sensitivity *= dust_im

    if show:
        show_image(sensitivity, cmap='gray', title=title)

    return sensitivity
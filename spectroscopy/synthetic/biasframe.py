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

def synthetic_image(dimensions, show=False, title="Synthetic Image"):
    """

    :param dimensions: List of two values
    :param show: bool [if print image directly]
    :return: numpy array [image]
    """
    synthetic_image = np.zeros(dimensions)
    if show:
        show_image(synthetic_image, cmap='gray', title=title)
    return synthetic_image


# Let's add some read noise
def read_noise(image, amount, gain=1, show=False, title='Read Noise'):
    """
    Generate simulated read noise

    :param image: numpy array [shape to match]
    :param amount: float [electrons]
    :param gain: float, optional [electrons/ADU]
    :param show: bool [if print image directly]
    :param title: String [Title of frame]
    :return: [noise array]
    """
    shape = image.shape
    noise = noise_rng.normal(scale=amount/gain, size=shape)
    if show:
        show_image(noise, cmap='gray', title=title)

    return noise

#plt.figure()
#noise_im = synthetic_image + read_noise(synthetic_image, 5)
#show_image(noise_im, cmap='gray')


# Let's create a bias image
def bias(image, value, realistic=False, show=False, title='Bias'):
    """
    Generate simulated bias image.

    :param image: numpy array [image whose shape to match]
    :param value: float [bias level]
    :param realistic: bool, optional [adds some columns with higher bias value]
    :return: numpy array [output bias image]
    """

    # The bias is supposed to be a constant offset!
    bias_im = np.zeros_like(image) + value

    # If we want a more realistic bias
    if realistic:
        shape = image.shape
        number_of_columns = 5

        # Let's use some randomness. BUT the bias should not change from image to image, therefore "constant" randomness
        rng = np.random.RandomState(seed=8392)
        columns = rng.randint(0, shape[1], size=number_of_columns)
        # Some random-looking noise
        col_pattern = rng.randint(0, int(0.1 * value), size=shape[0])

        for c in columns:
            bias_im[:, c] = value + col_pattern
    if show:
        show_image(bias_im, cmap='gray', title=title)
    return bias_im

#bias_only = bias(synthetic_image, 1100, realistic=True)
#show_image(bias_only, cmap='gray', figsize=(10, 10), title="Realisitc bias frame (with read noise)")

#bias_noise_im = noise_im + bias_only
#show_image(bias_noise_im, cmap='gray', figsize=(10, 10), title='Realistic bias frame (includes read noise)')


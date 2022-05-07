from spectroscopy.synthetic import biasframe
from spectroscopy.synthetic import darkframe
from spectroscopy.synthetic import sky_background
from spectroscopy.synthetic import flatfield

from spectroscopy.convenience_functions import show_image
import numpy as np

""" Single data
synth = biasframe.synthetic_image([1000, 1000])
read = biasframe.read_noise(synth, 5)
bias_only = biasframe.bias(read, 1000, realistic=True)
bias_frame = read + bias_only
#show_image(bias_frame, cmap='gray', title='Bias Frame')


dark_only = darkframe.dark_current(bias_frame, 0.1, 100, hot_pixels=True)
dark_frame = bias_frame + dark_only
#show_image(dark_frame, cmap='gray', title='Dark Frame')

sky_level = 20
sky_only = sky_background.sky_background(synth, sky_level)
sky_frame = sky_only + dark_frame
#show_image(all_considered, cmap='gray', title='All considered')

stars_only = sky_background.stars(synth, 50, max_counts=2000)
stars_frame = stars_only + dark_frame
#show_image(stars_frame, cmap='gray', title="Star Field")

flat_only = flatfield.flat(synth)
complete_image = stars_frame + flat_only
#show_image(complete_image, cmap='gray', title="Star Field Complete")
"""

# This is the complete reconstruction:

gain = 1.0
exposure = 30.0
dark = 0.1
sky_counts = 20
bias_level = 1100
read_noise_electrons = 5
max_star_counts = 2000

image = np.zeros([2000, 2000])

bias_only = biasframe.bias(image, bias_level, realistic=True)
noise_only = biasframe.read_noise(image, read_noise_electrons, gain=gain)
dark_only = darkframe.dark_current(image, dark, exposure, gain=gain, hot_pixels=True)
sky_only = sky_background.sky_background(image, sky_counts, gain=gain)
stars_only = sky_background.stars(image, 50, max_counts=max_star_counts)
flat_only = flatfield.flat(image)

final_image = bias_only + noise_only + dark_only + flat_only * (sky_only + stars_only)
show_image(final_image, cmap='gray', percu=99.9)

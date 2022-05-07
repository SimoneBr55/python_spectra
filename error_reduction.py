import numpy as np
from matplotlib import pyplot as plt

from spectroscopy.convenience_functions import show_image, show_image_manual
from spectroscopy.synthetic.biasframe import read_noise, bias
from spectroscopy.synthetic.darkframe import dark_current
from spectroscopy.synthetic.image_defects import sensitivity_variations
from spectroscopy.synthetic.sky_background import stars

from astropy.visualization import hist
from astropy.stats import histogram
"""
image = np.zeros([2000, 2000])
gain = 1.0
noise_amount = 1500

stars_with_noise = stars(image, 50, max_counts=2000, fwhm=10) + read_noise(image, noise_amount, gain=gain)

show_image_manual(stars_with_noise, cmap='gray', percu=99.9)
plt.title('Stars with noise')
incorrect_attempt_to_remove_noise = stars_with_noise - read_noise(image, noise_amount, gain=gain)
show_image_manual(incorrect_attempt_to_remove_noise, cmap='gray', percu=99.9)
"""



gain = 1.0
noise_amount = 1500
star_exposure = 30.0
dark_exposure = 60.0
dark = 0.1
sky_counts = 20
bias_level = 1100
read_noise_electrons = 700
max_star_counts = 2000

image = np.zeros([2000, 2000])

stars_with_noise = stars(image, 50, max_counts=2000, fwhm=10) + read_noise(image, noise_amount, gain=gain)

bias_with_noise = (bias(image, bias_level, realistic=True) +
                   read_noise(image, read_noise_electrons, gain=gain))

dark_frame_with_noise = (bias(image, bias_level, realistic=True) +
                         dark_current(image, dark, dark_exposure, gain=gain, hot_pixels=True) +
                         read_noise(image, read_noise_electrons, gain=gain))

flat = sensitivity_variations(image)

realistic_stars = (stars(image, 50, max_counts=max_star_counts) +
                   dark_current(image, dark, star_exposure, gain=gain, hot_pixels=True) +
                   bias(image, bias_level, realistic=True) +
                   read_noise(image, read_noise_electrons, gain=gain)
                  )


show_image(realistic_stars, cmap='gray', percu=99.9)

scaled_dark_current = star_exposure * (dark_frame_with_noise - bias_with_noise) / dark_exposure

calibrated_stars = (realistic_stars - bias_with_noise - scaled_dark_current) / flat

show_image(calibrated_stars, cmap='gray', percu=99.9)

plt.figure(figsize=(9, 9))
hist(calibrated_stars.flatten(), bins='freedman', label='calibrated star image', alpha=0.5)
hist(stars_with_noise.flatten(), bins='freedman', label='raw star image', alpha=0.5)
plt.legend()
plt.grid()
plt.xlabel('Count level in image')
plt.ylabel('Number of pixels with that count');
plt.show()
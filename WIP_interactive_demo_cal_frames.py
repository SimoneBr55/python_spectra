from ipywidgets import interactive, interact

import numpy as np
from spectroscopy.convenience_functions import show_image
from spectroscopy.synthetic.darkframe import dark_current
from spectroscopy.synthetic.biasframe import read_noise, bias
from spectroscopy.synthetic.sky_background import sky_background


# @interact(bias_level=(1000,1200,10), dark=(0.01,1,0.01), sky_counts=(0, 300, 10),
#           gain=(0.5, 3.0, 0.1), read=(0, 50, 2.0),
#           exposure=(0, 300, 10))
def complete_image(bias_level=1100, read=10.0, gain=1, dark=0.1,
                   exposure=30, hot_pixels=True, sky_counts=200):
    synthetic_image = np.zeros([500, 500])
    show_image(synthetic_image +
               read_noise(synthetic_image, read) +
               bias(synthetic_image, bias_level, realistic=True) +
               dark_current(synthetic_image, dark, exposure, hot_pixels=hot_pixels) +
               sky_background(synthetic_image, sky_counts),
               cmap='gray',
               figsize=None)


i = interactive(complete_image, bias_level=(1000, 1200, 10), dark=(0.0, 1, 0.1), sky_counts=(0, 300, 50),
                gain=(0.5, 3.0, 0.25), read=(0, 50, 5.0),
                exposure=(0, 300, 30))

for kid in i.children:
    try:
        kid.continuous_update = False
    except KeyError:
        pass
i
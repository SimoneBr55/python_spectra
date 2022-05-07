from spectroscopy.synthetic import biasframe
from spectroscopy.synthetic import darkframe

from spectroscopy.convenience_functions import show_image

#""" Show Bias
synth = biasframe.synthetic_image([1000, 1000])
read = biasframe.read_noise(synth, 5)
bias = biasframe.bias(read, 1000, realistic=True)
bias_frame = read + bias
show_image(bias_frame, cmap='gray', title='Bias Frame')
#"""

dark_only = darkframe.dark_current(bias_frame, 0.1, 100, hot_pixels=True)
dark_frame = bias_frame + dark_only
show_image(dark_frame, cmap='gray', title='Dark Frame')





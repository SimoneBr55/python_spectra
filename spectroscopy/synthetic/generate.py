from pathlib import Path
from itertools import cycle

import numpy as np
from astropy.nddata import CCDData


def fake_images(data_directory='/tmp/astropy'):
    image_path = Path(data_directory)
    image_path.mkdir(parents=True, exist_ok=True)

    images_to_generate = {
        'BIAS': 5,
        'DARK': 10,
        'FLAT': 3,
        'LIGHT': 10
    }

    exposure_times = {
        'BIAS': [0.0],
        'DARK': [5.0, 30.0],
        'FLAT': [5.0, 6.1, 7.3],
        'LIGHT': [30.0],
    }
    filters = {
        'FLAT': 'V',
        'LIGHT': 'V'
    }

    objects = {
        'LIGHT': ['m82', 'xx cyg']
    }

    image_size = [300, 200]

    image_number = 0
    for image_type, num in images_to_generate.items():
        exposures = cycle(exposure_times[image_type])
        try:
            filts = cycle(filters[image_type])
        except KeyError:
            filts = []

        try:
            objs = cycle(objects[image_type])
        except KeyError:
            objs = []
        for _ in range(num):
            img = CCDData(data=np.random.randn(*image_size), unit='adu')
            img.meta['IMAGETYP'] = image_type
            img.meta['EXPOSURE'] = next(exposures)
            if filts:
                img.meta['FILTER'] = next(filts)
            if objs:
                img.meta['OBJECT'] = next(objs)
            image_name = str(image_path / f'img-{image_number:04d}.fits')
            img.write(image_name)
            print(image_name)
            image_number += 1

fake_images()
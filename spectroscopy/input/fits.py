from pathlib import Path
from astropy.nddata import CCDData
from astropy.io import fits

from ccdproc import ImageFileCollection
"""
### PROVVISORIO ###
"""
def open_single_io(image_directory, image_name):

    image_path = Path(image_directory) / image_name

    hdu_list = fits.open(image_path)
    print(hdu_list.info())

    hdu = hdu_list[0]
    print(hdu.header)
    print(type(hdu.data))

def open_single_ccd(image_directory, image_name):
    image_path = Path(image_directory) / image_name

    ccd = CCDData.read(image_path)
    print(ccd.header)
    print(type(ccd.data))

def open_directory_ifc(data_directory):
    im_collection = ImageFileCollection(data_directory)

    print(im_collection.summary)

    for a_flat in im_collection.hdus(imagetyp='FLAT'):
        print(a_flat.header['EXPOSURE'])

    for a_flat, fname in im_collection.hdus(imagetyp='LIGHT', object='m82', return_fname=True):
        print(f'In file {fname} the exposure is: ', a_flat.header['EXPOSURE'], ' with standard deviation ', a_flat.data.std())

    for a_flat, fname in im_collection.ccds(bunit='ADU', return_fname=True):
        print(a_flat.unit)

    print(a_flat.header)

#open_single_io('/tmp/astropy', 'img-0001.fits')
#open_single_ccd('/tmp/astropy', 'img-0001.fits')
open_directory_ifc('/tmp/astropy')
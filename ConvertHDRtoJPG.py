import imageio

import os, json, logging, time, random
from math import sqrt
from collections import namedtuple
from PIL import Image
import numpy
#import OpenEXR
#import Imath


### HDR to JPG

def convert_hdr_to_jpg(filepath):
    if not os.path.isfile(filepath):
        return False

    directory = os.path.dirname(filepath)
    filename, extension = os.path.splitext(filepath)
    if not extension.lower() in ['.hdr', '.hdri']:
        return False

    imageio.plugins.freeimage.download()  #DOWNLOAD IT
    image = imageio.imread(filepath, format='HDR-FI')
    output = os.path.join(directory, filename + '.jpg')
    imageio.imwrite(output, image)


convert_hdr_to_jpg("F:\\\\_3D_Resource\\HDRI\\_Mini\\Breaking Dawn - Frosty Mornig_Mini.hdr")
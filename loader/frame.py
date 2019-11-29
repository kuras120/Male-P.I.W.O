import os

import numpy as np
from PIL import Image

from loader import LED_MATRIX_RESOLUTION


def load_frame(path: str):
    """
    Loads bitmap file and converts it to 3D numpy array
    :param path: the path to file
    :return: 3d nn
    """
    frame_img = Image.open(path)
    return np.array(frame_img)


def resize_to_resolution(path: str, resolution: (int, int)) -> None:
    """
    Resize image file to given resolution, and save the image in bitmap format
    :param path: the path to image file
    :param resolution: the tuple with (width, height) resolution
    :return:
    """
    img = Image.open(path)
    img.thumbnail(resolution, Image.ANTIALIAS)
    try:
        img = Image.open(path)
        img.thumbnail(resolution, Image.ANTIALIAS)
        img.save(path, 'BMP')
    except IOError:
        print("Cannot resize file ", path)


def resize_animation_frames(animation_dir: str) -> None:
    """
    Resize all of the files in animation directory to match LED_MATRIX_RESOLUTION
    :param animation_dir: the path to animation directory
    :return:
    """
    for file in os.listdir(animation_dir):
        if file.endswith(".bmp"):
            resize_to_resolution(os.path.join(animation_dir, file), LED_MATRIX_RESOLUTION)

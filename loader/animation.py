import json
import ntpath
import os
import zipfile

from loader import ANIMATIONS_ROOT_DIR
from loader.frame import resize_animation_frames, load_animation_frames


class AnimationMeta:
    """
    Represents the metadata of animation
    """
    def __init__(self, **kwargs):
        self.frame_count = 0,
        self.frame_duration = 0
        self.music_file = ""
        self.animation_name = ""
        self.description = ""
        self.__dict__.update(kwargs)


class Animation:
    def __init__(self, meta, frames):
        self.meta: AnimationMeta = meta
        self.frames = frames


def unzip_animation_file(file_path: str) -> str:
    """
    Extracts the animation file to a separate folder in ANIMATIONS_ROOT_DIR and returns the root path to animation
    :param file_path:
    :return:
    """
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(ANIMATIONS_ROOT_DIR)
    return os.path.join(ANIMATIONS_ROOT_DIR, extract_file_name(file_path))


def path_leaf(path: str) -> str:
    """
    Gets the leaf of the path: /home/user/file.txt -> file.txt
    :param path: the path to a file
    :return:
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def extract_file_name(path: str) -> str:
    """
    Extracts the filename without extension from path
    :param path: the path to file
    :return: filename
    """
    leaf = path_leaf(path)
    return os.path.splitext(leaf)[0]


def load_meta(animation_dir: str) -> AnimationMeta:
    meta_path = os.path.join(animation_dir, 'meta_template.json')
    with open(meta_path) as f:
        meta_dict = json.load(f)
        return AnimationMeta(**meta_dict)


def load_animation(path: str) -> Animation:
    animation_dir = unzip_animation_file(path)
    resize_animation_frames(animation_dir)
    meta: AnimationMeta = load_meta(animation_dir)
    frames = load_animation_frames(animation_dir)
    return Animation(meta, frames)


# anim_path = os.path.join(ANIMATIONS_ROOT_DIR, 'test_animation.zip')
# print(load_animation(anim_path).meta.__dict__)

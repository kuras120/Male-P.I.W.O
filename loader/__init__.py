import os
from pathlib import Path

LOADER_DIR = os.path.dirname(os.path.abspath(__file__))
ANIMATIONS_ROOT_DIR: str = os.path.join(Path(LOADER_DIR).parents[0], 'animations')

LED_MATRIX_RESOLUTION = 32, 16

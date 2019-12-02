#!/usr/bin/env python3
import os
import sys
import time
from random import randrange

from matrix.bindings.python.samples.samplebase import SampleBase
from matrix.bindings.python.rgbmatrix import RGBMatrixOptions

from loader import ANIMATIONS_ROOT_DIR
from loader.animation import AnimationMeta, load_animation, Animation, path_leaf, extract_file_name
from sound.bt import play_sound_in_background


class Piwo(SampleBase):
    def __init__(self, meta, frames, *args, **kwargs):
        self.meta: AnimationMeta = meta
        self.frames = frames
        super(Piwo, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        while True:
            for frame in self.frames:
                self.draw_frame(offset_canvas, frame, self.meta.frame_duration)

    def draw_frame(self, offset_canvas, matrix, period_time):
        start = time.time()
        for y in range(0, offset_canvas.height):
            for x in range(0, self.matrix.width):
                offset_canvas.SetPixel(
                    x, y, matrix[y][x][0], matrix[y][x][1], matrix[y][x][2])
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        end = time.time()
        print("Draw time: {}".format(end - start))
        time.sleep(0.002)


if __name__ == "__main__":
    # sudo python runtext.py  --led-no-hardware-pulse=true --led-slowdown-gpio=2 --led-rows=16 --led-cols=32 --led-pwm-lsb-nanoseconds=500

    if len(sys.argv) < 2:
        sys.exit("Require an image argument")
    else:
        animation_file_path = sys.argv[1]

    animation: Animation = load_animation(animation_file_path)
    sound_path = os.path.join(ANIMATIONS_ROOT_DIR, extract_file_name(animation_file_path), animation.meta.music_file)
    play_sound_in_background(sound_path, 0.5)
    simple_square = Piwo(animation.meta, animation.frames)

    if not simple_square.process():
        simple_square.print_help()

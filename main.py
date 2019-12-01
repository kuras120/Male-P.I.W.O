#!/usr/bin/env python3
import os
import time
from random import randrange

from matrix.bindings.python.samples.samplebase import SampleBase

from loader import ANIMATIONS_ROOT_DIR
from loader.animation import AnimationMeta, load_animation, Animation


class SimpleSquare(SampleBase):
    def __init__(self, meta, frames, *args, **kwargs):
        self.meta: AnimationMeta = meta
        self.frames = frames
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        while True:
            for frame in self.frames:
                self.draw_frame(offset_canvas, frame, self.meta.frame_duration)

    def draw_frame(self, offset_canvas, matrix, period_time):
        for y in range(0, offset_canvas.height):
            for x in range(0, self.matrix.width):
                offset_canvas.SetPixel(
                    x, y, matrix[y][x][0], matrix[y][x][1], matrix[y][x][2])
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        time.sleep(period_time)

    def get_frames(self, offset_canvas):
        frames = []
        for i in range(5):
            matrix = []
            for y in range(0, offset_canvas.height):
                matrix.append([])
                for x in range(0, offset_canvas.width):
                    led = {"r": randrange(256), "g": randrange(256), "b": randrange(256)}
                    matrix[y].append(led)
            frame = {"time": 5, "matrix": matrix}
            frames.append(frame)
        return frames

    # Main function


if __name__ == "__main__":
    # sudo python runtext.py  --led-no-hardware-pulse=true --led-slowdown-gpio=2 --led-rows=16 --led-cols=32 --led-pwm-lsb-nanoseconds=500
    anim_path = os.path.join(ANIMATIONS_ROOT_DIR, 'test_animation.zip')
    animation: Animation = load_animation(anim_path)
    simple_square = SimpleSquare(animation.meta, animation.frames)
    if not simple_square.process():
        simple_square.print_help()

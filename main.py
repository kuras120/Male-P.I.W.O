#!/usr/bin/env python3
import argparse
import sys
import time

from loader.animation import AnimationMeta, Animation, unzip_animation_file, \
    load_meta
from loader.frame import resize_animation_frames, load_animation_frames
from matrix.bindings.python.rgbmatrix import RGBMatrixOptions, RGBMatrix


class MiniPiwo(object):
    meta: AnimationMeta
    frames: list
    matrix: RGBMatrix

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-f", "--file", action="store", default="", type=str)

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def load_animation(self, path: str) -> Animation:
        print("Extracting animation file...")
        animation_dir = unzip_animation_file(path)
        print("Adjusting frames file...")
        resize_animation_frames(animation_dir)
        print("Loading meta...")
        meta: AnimationMeta = load_meta(animation_dir)
        print("Loading frames...")
        frames = load_animation_frames(animation_dir)
        return Animation(meta, frames)

    def init_from_args(self):
        self.args = self.parser.parse_args()
        self.load_animation(self.args.file)
        options = RGBMatrixOptions()

        options.rows = 16
        options.cols = 32
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        options.pwm_lsb_nanoseconds = 500
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.disable_hardware_pulsing = True
        options.gpio_slowdown = 2
        options.show_refresh_rate = 1

        self.matrix = RGBMatrix(options=options)

    def process(self):
        self.init_from_args()
        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

    def run(self):
        print("Running")
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
    piwo = MiniPiwo()
    if not piwo.process():
        piwo.print_help()

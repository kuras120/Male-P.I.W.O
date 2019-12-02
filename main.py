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
        self.parser.add_argument("-r", "--led-rows", action="store", default=16, type=int)
        self.parser.add_argument("--led-cols", action="store", default=32, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store", default=1, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store", default=100, type=int)
        self.parser.add_argument("--led-scan-mode", action="store", default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", default=500, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true")
        self.parser.add_argument("--led-slowdown-gpio", action="store", default=2, type=int)
        self.parser.add_argument("--led-rgb-sequence", action="store", default="RGB", type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store", default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store", default=0, type=int, choices=[0, 1, 2])
        self.parser.add_argument("--led-multiplexing", action="store", default=0, type=int)

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

        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper
        if self.args.led_show_refresh:
            options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio is not None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True

        self.matrix = RGBMatrix(options=options)

    def process(self):
        self.init_from_args()
        self.load_animation()
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

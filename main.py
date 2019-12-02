#!/usr/bin/env python3
import argparse
import os
import sys
import time

from loader import ANIMATIONS_ROOT_DIR
from loader.animation import AnimationMeta, unzip_animation_file, load_meta, extract_file_name
from loader.frame import resize_animation_frames, load_animation_frames
from matrix.bindings.python.rgbmatrix import RGBMatrixOptions, RGBMatrix
from sound.bt import play_sound_in_background


class MiniPiwo(object):
    meta: AnimationMeta
    frames: list
    matrix: RGBMatrix
    root_path: str

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-f", "--file", action="store", default="",
                                 help="The path to zipped animation file", type=str)
        self.parser.add_argument("-r", "--led-rows", action="store",
                                 help="Display rows. 16 for 16x32, 32 for 32x32. Default: 16", default=16, type=int)
        self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)",
                                 default=32, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 1.",
                                 default=1, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store",
                                 help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store",
                                 help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store",
                                 help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)
        self.parser.add_argument("-m", "--led-gpio-mapping",
                                 help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm",
                                 choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self.parser.add_argument("--led-scan-mode", action="store",
                                 help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)",
                                 default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store",
                                 help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 500",
                                 default=500, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true",
                                 help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument("--led-slowdown-gpio", action="store",
                                 help="Slow down writing to GPIO. Range: 0..4. Default: 2", default=2, type=int)
        self.parser.add_argument("--led-no-hardware-pulse", action="store",
                                 help="Don't use hardware pin-pulse generation. Default: True", default=True)
        self.parser.add_argument("--led-rgb-sequence", action="store",
                                 help="Switch if your matrix has led colors swapped. Default: RGB", default="RGB",
                                 type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"",
                                 default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store",
                                 help="0 = default; 1=AB-addressed panels;2=row direct", default=0, type=int,
                                 choices=[0, 1, 2])
        self.parser.add_argument("--led-multiplexing", action="store",
                                 help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven (Default: 0)",
                                 default=0, type=int)

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def load_animation(self, path: str) -> None:
        print("Extracting animation file...")
        animation_dir = unzip_animation_file(path)
        print("Adjusting frames file...")
        resize_animation_frames(animation_dir)
        print("Loading meta...")
        self.meta = load_meta(animation_dir)
        print("Loading frames...")
        self.frames = load_animation_frames(animation_dir)

    def init_from_args(self) -> None:
        self.args = self.parser.parse_args()
        self.load_animation(self.args.file)
        self.root_path = os.path.join(ANIMATIONS_ROOT_DIR, extract_file_name(self.args.file))
        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping is not None:
            options.hardware_mapping = self.args.led_gpio_mapping
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

    def process(self) -> bool:
        self.init_from_args()
        play_sound_in_background(os.path.join(self.root_path, self.meta.music_file), 0.5)
        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

    def run(self) -> None:
        print("Running")
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


if __name__ == "__main__":
    piwo = MiniPiwo()
    if not piwo.process():
        piwo.print_help()

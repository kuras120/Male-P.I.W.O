#!/usr/bin/env python3
from matrix.bindings.python.samples.samplebase import SampleBase
import time
from random import randrange


class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        while True:
            frames = self.get_frames(offset_canvas)
            for frame in frames:
                self.draw_frame(offset_canvas, frame["matrix"], frame["time"])

    def draw_frame(self, offset_canvas, matrix, period_time):
        for y in range(0, offset_canvas.height):
            for x in range(0, self.matrix.width):
                offset_canvas.SetPixel(
                    x, y, matrix[y][x]["r"], matrix[y][x]["g"], matrix[y][x]["b"])
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
    simple_square = SimpleSquare()
    if not simple_square.process():
        simple_square.print_help()

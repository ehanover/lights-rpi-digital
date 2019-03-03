#import time
import board
import neopixel
import sys

pixel_pin = board.D12
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=True, pixel_order=ORDER)

c = [int(i) for i in sys.argv[1:]]

pixels.fill(tuple(c))


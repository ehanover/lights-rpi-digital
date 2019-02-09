import time
import board
import neopixel
import sys
#from collections import deque

pixel_pin = board.D18
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

while True:

	pixels.show()
	time.sleep(sleep)

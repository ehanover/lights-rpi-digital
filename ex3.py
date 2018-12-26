# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 60

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=True, pixel_order=ORDER)

pixels.fill((0,0,1))


bump = [(10, 10, 10), (5, 200, 5), (10, 10, 10)]


for i in range(num_pixels):
	pixels[i] = (0, 0, 200)
	pixels.show()
	time.sleep(0.1)

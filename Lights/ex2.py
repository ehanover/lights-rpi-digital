# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18. NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 60

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed! For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=True, pixel_order=ORDER)

pixels.fill((0,0,1))


colors = []
inc = 255.0/num_pixels
for j in range(num_pixels):
	c = inc*j
	colors.append( (j, 0, 255-j) )

for index in range(num_pixels):

	for i in range(num_pixels):
		c_i = i+index
		if c_i >= num_pixels:
			c_i -= num_pixels

		pixels[i] = colors[c_i]
	pixels.show()
	time.sleep(0.001)


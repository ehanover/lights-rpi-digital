import time
import board
import neopixel
import sys
from collections import deque

pixel_pin = board.D18
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

colors = []
for i in sys.argv[3:]:
	colors.append( [int( (i[a]+i[a+1] ), 16) for a in range(0, len(i), 2)] )
#colors = [ [255,0,0], [0,255,0], [0,0,255] ]
#colors = [ [0,255,0], [0,0,0], [0,0,0] ]
#colors = [ [255,0,0], [255,0,255], [0,0,2] ]
#colors = [ [255,0,0], [0,0,0], [0,255,0], [0,0,0], [0,0,255], [0,0,0] ]

sleep = float(sys.argv[1])
tick = int(sys.argv[2])
#sleep = 0.009 # speed
#tick = 50 # increment

pix = deque([[0,0,0] for i in range(num_pixels)], maxlen=num_pixels)
ci = 0
cur = colors[ci]
t = tick

while True:

	if t == tick:
		ci += 1
		if ci >= len(colors):
			ci = 0

		d = [ (colors[ci][a]-cur[a])/t for a in range(3) ]
		t = 0

	cur = [ cur[a]+d[a] for a in range(3) ]
	t += 1

	#print( tuple([int(a) for a in cur] )
	pix.append( [int(a) for a in cur] )
	#pixels.fill( tuple([int(a) for a in cur]) )
	for i in range(num_pixels):
		pixels[i] = tuple(pix[i])

	pixels.show()
	time.sleep(sleep)

import time
import board
import neopixel
import sys
from collections import deque

pixel_pin = board.D12
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

colors = []
for i in sys.argv[4:]:
	colors.append( [int( (i[a]+i[a+1] ), 16) for a in range(0, len(i), 2)] )
#colors = [ [255,0,0], [0,255,0], [0,0,255] ]
#colors = [ [0,255,0], [0,0,0], [0,0,0] ]
#colors = [ [255,0,0], [255,0,255], [0,0,2] ]
#colors = [ [255,0,0], [0,0,0], [0,255,0], [0,0,0], [0,0,255], [0,0,0] ]

center = (int(sys.argv[3]) == 1)
sleep = float(sys.argv[1])
tick = int(sys.argv[2])
#sleep = 0.009 # speed
#tick = 50 # increment

num_pix_deque = int(num_pixels/2) if center else num_pixels
pix_deque = deque([[0,0,0] for i in range(num_pix_deque)], maxlen=num_pix_deque) # pix is the deque that holds rgb values for each light. The oldest value gets bumped out every frame.
ci = 0 # ci is the index of the current user-given color
cur = colors[ci] # cur is the current color values, in [r,g,b]
t = tick # t increments every frame. Every "tick" increments of t, the d values are recalculated to fade to the next color. 

while True:

	if t == tick:
		ci += 1
		if ci >= len(colors):
			ci = 0

		d = [ (colors[ci][a]-cur[a])/t for a in range(3) ] # d represents what has to be added to the color values every frame. It is recalculated every "tick" increments of t.
		t = 0

	cur = [ cur[a]+d[a] for a in range(3) ]
	t += 1

	#print( tuple([int(a) for a in cur] )
	pix_deque.append( [int(a) for a in cur] )
	#pixels.fill( tuple([int(a) for a in cur]) )

	if center:
		for i in range(num_pix_deque):
			pixels[i] = tuple(pix_deque[i])
			pixels[num_pixels-1-i] = tuple(pix_deque[i])
	else:
		for i in range(num_pixels):
			pixels[i] = tuple(pix_deque[i])

	pixels.show()
	time.sleep(sleep)

import time
import board
import neopixel
import sys
#from collections import deque

pixel_pin = board.D12
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=True, pixel_order=ORDER)

curr = [0, 0, 0]
add = [1, 0, 1]
while True:
    curr = [curr[i] + add[i] for i in range(len(curr))]

    if curr[0] >= 255:
        curr = [0,0,0]
    print(curr)
    pixels.fill((curr[0], curr[1], curr[2]))
    #pixels.show()
    
    time.sleep(0.8)


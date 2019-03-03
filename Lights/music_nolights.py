import time
#import board
#import neopixel
import sys

#pixel_pin = board.D18
num_pixels = 60
#ORDER = neopixel.GRB
#pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=True, pixel_order=ORDER)


import numpy as np
#from Visualizer.MicrophoneRecorder import MicrophoneRecorder
from MicrophoneRecorder import MicrophoneRecorder

SCALE = 0.08
FMAX = 2000 # max frequency at dlen=257
DLEN = 257

SECTIONS = [
        [0, 150],
        [151, 710],
        [711, FMAX]
]
SECTION_SIZES = [SECTIONS[i][1]-SECTIONS[i][0] for i in range(len(SECTIONS))]
SECTION_WEIGHTS = [.65, 0.9, 1.2]


#pixels.fill((0,10,10))

def get_volumes(freqs):

        data = np.abs( np.fft.rfft(freqs[-1]) )
        avg = [0]*len(SECTIONS)

        for i in range(len(data)):

                f = (i/DLEN)*FMAX # guessed frequency
                for s in range(len(SECTIONS)):
                        if SECTIONS[s][0] <= f <= SECTIONS[s][1]:
                                avg[s] += int(data[i])
                                break

        return [int( SECTION_WEIGHTS[i]*avg[i]/SECTION_SIZES[i] ) for i in range(len(SECTIONS))]


r = MicrophoneRecorder(rate=8000, chunksize=512)
vals = [0,0,0]

while True:

        freqs = r.get_frames()
        if len(freqs) > 0:
                vals = [ int( min(max(i*SCALE, 0), 255) ) for i in get_volumes(freqs) ]
                #print("updating colors")
                print(vals)

                #pixels.fill(tuple(vals)) # assumes there are 3 sections
                #pixels.fill(( vals[0], vals[1], vals[2] ))
                #pixels.fill(( 10,0,0 ))

        #pixels.show()
        #time.sleep(0.001)



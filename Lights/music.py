import time
import board
import neopixel
import sys

pixel_pin = board.D18
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)


import numpy as np
from Visualizer.MicrophoneRecorder import MicrophoneRecorder

SCALE = 0.01
FMAX = 2000 # max frequency at dlen=257
DLEN = 257

SECTIONS = [
	[0, 150],
	[151, 710],
	[711, FMAX]
]
SECTION_SIZES = [SECTIONS[i][1]-SECTIONS[i][0] for i in range(len(SECTIONS))]
SECTION_WEIGHTS = [.7, 0.9, 1.2]


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
		vals = [ min( max(i*SCALE, 2), 255) for i in get_volumes(freqs) ]

	pixels.fill(tuple(vals)) # assumes there are 3 sections

	pixels.show()
	time.sleep(sleep)

# r.close() might go here. MicrophoneRecorder calls close with atexit
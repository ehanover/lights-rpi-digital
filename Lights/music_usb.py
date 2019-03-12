'''
To get pyaudio to work with neopixel's usage of hardware pwm:
    edit /etc/modprobe.d/snd-blacklist.conf and add 
        blacklist snd_bcm2835
    edit /boot/config.txt and add 
        hdmi_force_hotplug=1 
        hdmi_force_edid_audio=1 
        hdmi_drive=2

I don't know which of those modifications are needed
'''

import time
import board
import neopixel
import sys
from collections import deque

pixel_pin = board.D12
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels_deque = deque([[0,0,0] for i in range(num_pixels)], maxlen=num_pixels) # pix is the deque that holds rgb values for each light. The oldest value gets bumped out every frame.

import numpy as np
#from Visualizer.MicrophoneRecorder import MicrophoneRecorder
from MicrophoneRecorder import MicrophoneRecorder

GLOBAL_SCALE = 0.05
FMAX = 2000 # max frequency at dlen=257
DLEN = 257

'''
SECTIONS = [
        [0, 150],
        [151, 710],
        [711, FMAX]
]
SECTION_WEIGHTS = [.8, 1, 1.5]

'''
# python3 music.py lower upper s1 s2 s3 b1 b2 b3 mode


SECTIONS = [ [0, int(sys.argv[1])], [int(sys.argv[1])+1, int(sys.argv[2])], [int(sys.argv[2])+1, FMAX] ] 
SECTION_SIZES = [SECTIONS[i][1]-SECTIONS[i][0] for i in range(len(SECTIONS))]

SCALES = []
BIASES = []

prev = 0
for i in range(3):
    SCALES.append(float(sys.argv[i+3])/100)
    BIASES.append(float(sys.argv[i+6]))

MODE = int(sys.argv[-1])

print("sections: " + str(SECTIONS))
print("scales: " + str(SCALES))
print("biases: " + str(BIASES))
print("mode: " + str(MODE))
#sys.exit(0)

pixels.fill((1,1,1))
pixels.show()

def get_volumes(freqs):

        data = np.abs( np.fft.rfft(freqs[-1]) )
        avg = [0]*len(SECTIONS)

        for i in range(len(data)):

                f = (i/DLEN)*FMAX # guessed frequency
                for s in range(len(SECTIONS)):
                        if SECTIONS[s][0] <= f <= SECTIONS[s][1]:
                                avg[s] += int(data[i])
                                break

        return [int( avg[i]/SECTION_SIZES[i] ) for i in range(len(SECTIONS))]


r = MicrophoneRecorder(rate=8000, chunksize=512)
#vals = [0,0,0]

while True:
    freqs = r.get_frames()
    if len(freqs) > 0:

        volumes = get_volumes(freqs)
        vals = []
        for i in range(len(volumes)):
            a = (volumes[i]*SCALES[i]*GLOBAL_SCALE) + BIASES[i]
            b = int( min(max(a,0), 255) )
            vals.append(b)
        #print(vals)

        if MODE == 0: # all of the lights are the same
            pixels.fill(tuple(vals)) # assumes 3 sections

        elif MODE == 1: # lights divided into physical sections for frequency sections
            for i in range(num_pixels):
                val_index = int((i/num_pixels)*len(SECTIONS))  
                val = vals[val_index]

                color = (0, 0, 0)
                if val_index == 0:
                    color = (val, 0, 0)
                elif val_index == 1:
                    color = (0, val, 0)
                elif val_index == 2:
                    color = (0, 0, val)

                pixels[i] = color

        elif MODE == 2: # "bass history" mode
            pixels_deque.append( [vals[0], 0, 0] )
            for i in range(num_pixels):
                pixels[i] = tuple(pixels_deque[i])

        pixels.show()

    else: # no frames available
        pass
#       if MODE == 2:
#            pixels_deque.append([0,0,0])
            #pass
#            time.sleep(0.01)

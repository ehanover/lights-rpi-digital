#import pyaudio
#import threading
#import atexit
import numpy as np
import pygame
from MicrophoneRecorder import MicrophoneRecorder


WIDTH = 800
HEIGHT = 440

FMAX = 2000 # max frequency at dlen=257
DLEN = 257 # 257
SKIP = 1
W = WIDTH/(DLEN/SKIP)

# SECTIONS = [
#     [0, 200],
#     [201, 700],
#     [701, 1300],
#     [1301, FMAX]
# ]
SECTIONS = [
    [0, 150],
    [151, 710],
    [711, FMAX]
]
SECTION_SIZES = [SECTIONS[i][1]-SECTIONS[i][0] for i in range(len(SECTIONS))]
SECTION_WEIGHTS = [.7, 0.9, 1.2]

sw = 55

def draw(d, fs):

    d.fill((255, 255, 255))
   
    data = np.abs( np.fft.rfft(fs[-1]) )
    #data = np.sqrt(data)
    #print(len(data))

    avg = [0]*len(SECTIONS)

    for i in range(0, DLEN, SKIP):
        pygame.draw.rect(d, (10,100,200), (i*W, HEIGHT, W, -data[i]/450))
        #avg[int((i/DLEN)*SECTIONS)] += int(data[i])

        # add to section averages
        f = (i/DLEN)*FMAX # guessed frequency
        for s in range(len(SECTIONS)):
            if SECTIONS[s][0] <= f <= SECTIONS[s][1]:
                avg[s] += int(data[i])
                break
    
    # draw dividers for section groups
    for s in SECTIONS:
        for i in s:
            pygame.draw.rect(d, (110,0,0), (i*(WIDTH/FMAX)-3, HEIGHT, 6, -22))

    # draw bars for section average
    for i in range(len(SECTIONS)):
        pygame.draw.rect(d, (10,200,100), (i*sw, HEIGHT/2, sw-1, (-SECTION_WEIGHTS[i]*avg[i]/SECTION_SIZES[i])/40) )



r = MicrophoneRecorder(rate=8000, chunksize=512)

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('visualizer')
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    fs = r.get_frames()
    if len(fs) > 0:
        draw(display, fs)

    pygame.display.update()
    clock.tick(60)

r.close()
pygame.quit()

import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 30*2)

pixels.fill((0, 255, 0))
pixels[1] = (255, 0, 0)

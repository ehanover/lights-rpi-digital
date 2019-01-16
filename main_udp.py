import socket
import json

import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 30*2)
bright = 255

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('0.0.0.0', 50000)) # TODO this might not work. '0.0.0.0' was originally the ip of the computer running the server


try:
	while True:
		data, addr = s.recvfrom(1024)

		dj = json.loads(str(data))

		#print("data received: ", data)
		#s.sendto(data, addr)

		pixels.fill( (dj["x"]*bright, dj["y"]*bright, dj["z"]*bright) )
except: #KeyboardInterrupt
	s.close()
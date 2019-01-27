import socket
import json

import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 30*2)
bright = 100

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('0.0.0.0', 50000)) # TODO this might not work. '0.0.0.0' was originally the ip of the computer running the server

pixels.fill((0, 0, 0))

try:
	while True:
		data, addr = s.recvfrom(1024)
		#print("data: " + str(data))
		#print("d type: " + str(type(str(data))))

		#ds = str(data)
		ds = data.decode('utf-8')
		#print(ds)
		dj = json.loads(ds)

		c_list = [dj['x'], dj['y'], dj['z']]
		c_vals = [ min(int(abs(a)*bright), 255) for a in c_list]

		#print("data received: ", data)
		#s.sendto(data, addr)

		pixels.fill( (c_vals[0], c_vals[1], c_vals[2]) )
except KeyboardInterrupt:
	pixels.fill((0, 0, 0))
	s.close()

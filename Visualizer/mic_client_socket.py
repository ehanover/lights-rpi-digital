import time
import socket
#import struct
from MicrophoneRecorder import MicrophoneRecorder
#import numpy as np
import array

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.settimeout(.2)

addr = ('192.168.1.16', 50000)

r = MicrophoneRecorder(rate=8000, chunksize=512)

running = True
while running:

	frames = r.get_frames()

	if len(frames) > 0:
		#print("!!", list(frames[0]))
		#print("!!", len(frames[0]))
		#print(frames[-1][0:10])
		#print(max(frames[-1]))
		#message = bytearray(frames[-1])
		#message = bytes( frames[-1] )
		#message = struct.pack('f'*len(frames), *frames)
		#message = np.array(frames[-1]).tobytes()
		#message = bytes( array.array('B', [min(abs(i), 255) for i in frames[-1]] ).tobytes() )
		message = bytes( array.array('B', [int(abs(i)/128) for i in frames[-1]] ).tobytes() )
		#a = [ int(abs(i)).to_bytes(8, byteorder='big' , signed=False) for i in frames[-1] ]
		#message = bytes(a)
		#message = bytes([min(abs(i/8), 254) for i in frames[-1]])

		#decoded = list(message)
		#decoded = [int.from_bytes(d, byteorder='big', signed=False) for d in message]
		#print(decoded[0:10])
		
		socket.sendto(message, addr)
		#running = False
r.close()


	# try:
	# 	data, server = socket.recvfrom(1024)
	# 	end = time.time()
	# 	elapsed = end - start
	# 	print(f'received: d:{data} p:{pings} et:{elapsed}')

	# except: #socket.timeout
	# 	print('REQUEST TIMED OUT	', end="")

	# 	end = time.time()
	# 	elapsed = end - start
	# 	print("elapsed: {}".format(elapsed))
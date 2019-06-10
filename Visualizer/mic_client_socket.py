from MicrophoneRecorder import MicrophoneRecorder
import time
import socket
import array

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.settimeout(.2)
addr = ('192.168.1.10', 50000) # change this to the the pi's ip

r = MicrophoneRecorder(rate=8000, chunksize=512)

while True:

	frames = r.get_frames()

	if len(frames) > 0:

		message = bytes( array.array('B', [int(abs(i)/128) for i in frames[-1]] ).tobytes() )

        # other tries:
		#message = bytearray(frames[-1])
		#message = bytes( frames[-1] )
		#message = struct.pack('f'*len(frames), *frames)
		#message = np.array(frames[-1]).tobytes()
		#message = bytes( array.array('B', [min(abs(i), 255) for i in frames[-1]] ).tobytes() )
		#message = bytes([ int(abs(i)).to_bytes(8, byteorder='big' , signed=False) for i in frames[-1] ])
		#message = bytes([min(abs(i/8), 254) for i in frames[-1]])

		#decoded = list(message)
		#decoded = [int.from_bytes(d, byteorder='big', signed=False) for d in message]
		#print(decoded[0:10])
		
		socket.sendto(message, addr)

r.close()


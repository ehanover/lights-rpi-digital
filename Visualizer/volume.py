# import pyaudio
# import numpy as np

# CHUNK = 2**11
# RATE = 44100

# p=pyaudio.PyAudio()
# stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True, frames_per_buffer=CHUNK)

# for i in range(int(10*44100/1024)): #go for a few seconds
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#     peak = np.average(np.abs(data))*2
#     bars= " #"  int(50*peak/2**16)
#     print( "%04d %05d %s" % (i,peak,bars) )

# stream.stop_stream()
# stream.close()
# p.terminate()
# example: https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
# https://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic?noredirect=1&lq=1
import pyaudio # sudo apt install python3.5-pyaudio  check with pip3.5 install pyaudio
import struct
import math
import atexit



FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

pa = pyaudio.PyAudio()
stream = pa.open(format = FORMAT, 
		 channels = CHANNELS, 
		 rate = RATE, 
		 input = True,
		 input_device_index = 6,
		 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

def exit_func():
	print("exiting...")
	stream.stop_stream()
	stream.close()
	pa.terminate()
	print("there were {} errors.".format(errorcount))

def print_devices():
	info = pa.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')
	for i in range(0, numdevices):
		if (pa.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
			print( "Input Device id ", i, " - ", pa.get_device_info_by_host_api_device_index(0, i).get('name') )

def get_rms(block):
	# RMS amplitude is defined as the square root of the mean over time of the square of the amplitude. so we need to convert this string of bytes into  a string of 16-bit samples...

	# we will get one short out for each two chars in the string.
	count = len(block)/2
	format = "%dh"%(count)
	shorts = struct.unpack( format, block )

	# iterate over the block.
	sum_squares = 0.0
	for sample in shorts:
	# sample is a signed short in +/- 32768. 
	# normalize it to 1.0
		n = sample * SHORT_NORMALIZE
		sum_squares += n*n

	return math.sqrt( sum_squares / count )


atexit.register(exit_func)
print_devices()

errorcount = 0
for i in range(1000):
	try:
		block = stream.read(INPUT_FRAMES_PER_BLOCK)   
		amplitude = get_rms(block)

		print( "amp: {:.1f}".format(amplitude) )
		
	except IOError as e:
		errorcount += 1
		print( "(%d) Error recording: %s"%(errorcount,e) )

	
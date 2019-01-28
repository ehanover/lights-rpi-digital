import flask
from flask import Flask
from flask import request
import json
import subprocess as sp

import board
import neopixel


app = Flask(__name__)
app.config['DEBUG'] = False
app.config['ENV'] = 'development'

pixels = neopixel.NeoPixel(board.D18, 30*2)

pixels.fill((0, 1, 0))
#pixels[1] = (255, 0, 0)

current = sp.Popen(['echo', ' '])

def start(l):
	global current
	print(l)
	sp.Popen.terminate(current)
	current = sp.Popen(l)

@app.route('/off')
def off():
	start(['python3', 'solid.py', '0', '0', '0'])
	#global current
	#sp.Popen.terminate(current)
	#pixels.fill((0, 0, 0))

	print("lights off.")
	return "lights off.", 200

@app.route('/solid')
def solid():
	r = int(request.args.get("r"))
	g = int(request.args.get("g"))
	b = int(request.args.get("b"))

	start(['python3', 'solid.py', str(r), str(g), str(b)])
	#global current
	#sp.Popen.terminate(current)
	#pixels.fill((r, g, b))

	print("colors set")
	return "colors set.", 200

@app.route('/gyro')
def gyro():
	start(['python3', 'gyro_udp.py'])

	print("started gyro")
	return "started gyro.", 200

@app.route('/rainbow')
def rainbow():
	start(['python3', 'rainbow.py'])

	print("started rainbow")
	return "started rainbow.", 200

@app.route('/fade')
def fade():
	s = float(request.args.get("s"))
	t = int(float(request.args.get("t")))

	# Color(0xOORRGGBB)
	a = request.args.get("a")[10:-1]
	b = request.args.get("b")[10:-1]
	c = request.args.get("c")[10:-1]
	start(['python3', 'fade.py', str(s), str(t), str(a), str(b), str(c)])

	print("started fade")
	return "started fade.", 200

@app.route('/shutdown')
def shutdown():
	off()
	sp.Popen(['sudo', 'shutdown', '-h', 'now'])
	return "shutdown.", 200

if __name__ == "__main__":
	app.run(host='0.0.0.0')


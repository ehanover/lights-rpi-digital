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

pixels.fill((1, 1, 1))
#pixels[1] = (255, 0, 0)

current = sp.Popen(['echo', 'test'])

def start(l):
	global current
	sp.Popen.terminate(current)
	current = sp.Popen(l)

@app.route('/off')
def off():
	global current
	sp.Popen.terminate(current)
	pixels.fill((0, 0, 0))

	print("lights off.")
	return "lights off.", 200

@app.route('/solid')
def solid():
	global current
	sp.Popen.terminate(current)
	r = int(request.args.get("r"))
	g = int(request.args.get("g"))
	b = int(request.args.get("b"))

	pixels.fill((r, g, b))

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

	print("started fade")
	return "started fade.", 200

if __name__ == "__main__":
	app.run(host='0.0.0.0')


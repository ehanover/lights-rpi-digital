#import pyaudio
#import threading
#import atexit
import numpy as np

from MicrophoneRecorder import MicrophoneRecorder

r = MicrophoneRecorder()


#import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import random
#import tmp102

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# This function is called periodically from FuncAnimation
def animate(i):

    # Read temperature (Celsius) from TMP102
    #temp_c = round(tmp102.read_temp(), 2)
    #data = random.randint(0, 10)
    fs = r.get_frames()
    if len(fs) <= 0:
        return
    #data = fs[-1]    
    data = np.fft.rfft(fs[-1])    
    data = np.sqrt(data)

    # Add x and y to lists
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    #xs = dt.datetime.now().strftime('%H:%M:%S.%f')
    #ys.append(data)
    ys = data
    xs = np.arange(len(ys))

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)    
    #ax.plot(xs, 2000)

    # Format plot
    #plt.xticks(rotation=45, ha='right')
    #plt.subplots_adjust(bottom=0.30)
    #plt.title('TMP102 Temperature over Time')
    ax.set_ylim([-1000, 1000])
    #plt.ylabel('Y label')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=5) # fargs=(xs, ys), 
plt.show()

r.close()

# while True:
#     try:
#         fs = r.get_frames()
#         if len(fs) > 0:
#             f = fs[-1]

#             f_fft = np.fft.rfft(f)
#             print(f_fft)
#     except KeyboardInterrupt as e:
#         r.close()
#         break
    

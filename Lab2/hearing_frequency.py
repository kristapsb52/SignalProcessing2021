# %%
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
import soundfile

# %%
# https://www.linkedin.com/pulse/signal-processing-python-part-1-generate-signals-basic-hampiholi
# Create figure with 2 subplots, 2 rows and 1 column
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Sample rate of the periodic signal we will generate
Fs = 48000

# Time duration of the signals
t = np.linspace(0, 3, Fs, False) # 1/4 second

# Generate signal with 10 and 20 Hz frequency
sig1 = np.cos(2*np.pi*10*t)
sig2 = np.cos(2*np.pi*1*t)

# Plot the 10Hz signal in first subplot using default color line
ax1.plot(t, sig1)
ax1.set_title("10 Hz cos")
ax1.axis([0, 2, -1.5, 1.5])

# Plot the 20Hz signal in first subplot using red color line
ax2.plot(t, sig2, 'r')
ax2.set_title('20 Hz cos')
ax2.axis([0, 2, -1.5, 1.5])

plt.tight_layout()
plt.show()
# %%
soundfile.write("1hz_sample.wav", sig2, Fs)

# %%
# Creating .wav files with frequencies
sample_rate = 48000
frequencies = [100, 1000, 5000, 15000, 20000, 22000]
for frequency in frequencies:
    sig = np.cos(2*np.pi*frequency*t+(1/3*np.pi))
    
    soundfile.write(f"{frequency}Hz_sample.wav", sig, sample_rate)
# %%
# Playing back .wav files
# define stream chunk
chunk = 1024

# instantiate PyAudio
p = pyaudio.PyAudio()
for frequency in frequencies:
    f = wave.open(f"{frequency}HZ_sample.wav", "rb")
    # open Stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)
    
    #play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    
    #stop stream
    stream.stop_stream()
    stream.close()
    
# close PyAudio
p.terminate()
# %%

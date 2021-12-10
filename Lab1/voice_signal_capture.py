# %%

# To check which directory jupyter is located at
# import os
# print(os.getcwd())

# %%
# Note: It is not recommended to listen to the loud.wav file
# It is only made for the reason to see the frequency differences in spectrogram
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import soundfile

from scipy.io.wavfile import read
from scipy import signal

# %%
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "normal.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# %%
# https://stackoverflow.com/questions/44787437/how-to-convert-a-wav-file-to-a-spectrogram-in-python3

files = ["loud.wav", "normal.wav"]
for i in range(len(files)):
    sample_rate, samples = read(files[i])
    frequencies, times, spectrogram = signal.spectrogram(samples[50000:65000, 0], sample_rate)
    plt.subplot(1,2,i+1)
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
plt.show()
# %%
# Add noise to the normal.wav
noise = np.random.normal(100, 20, len(samples))
noisy_signal = samples[:, 0] + noise
# https://stackoverflow.com/questions/63898448/add-noise-to-audio-file-and-reconvert-the-noisy-signal-using-librosa-python
soundfile.write('noisy_normal.wav', noisy_signal, sample_rate)
# NOTE: IT IS NOT RECOMMENDED TO LISTEN TO THIS AUDIO FILE

# %%
# Inverting normal.wav
sample_rate, samples = read("normal.wav")
data = samples[::-1]
soundfile.write("inverted_normal.wav", data, samplerate=sample_rate)
# %%

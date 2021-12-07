import scipy.io
from scipy.signal import find_peaks

import numpy as np

import matplotlib.pyplot as plt

if __name__ == "__main__":
    ecg_mat = scipy.io.loadmat("ECG\ecgdemodata1.mat")
    ecg_wave_arr = ecg_mat['ecg'][0]
    samplingrate = ecg_mat['samplingrate'][0]
    
    # https://stackoverflow.com/questions/1713335/peak-finding-algorithm-for-python-scipy
    ecg_wave_peaks = find_peaks(ecg_wave_arr, prominence=500)
    
    avg_period = np.mean(np.diff(ecg_wave_peaks[0]))
    BPM =  60 * samplingrate / avg_period
    print(f"BPM: {BPM[0]}")
    
    plt.plot(ecg_wave_arr)
    plt.scatter(y=ecg_wave_arr[ecg_wave_peaks[0]], x=ecg_wave_peaks[0])
    plt.show()
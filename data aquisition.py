import numpy as np
import matplotlib.pyplot as plt
import rtl_sdr

# Set SDR parameters
CENTER_FREQ = 1420.4e6 # Hydrogen line frequency in Hz
SAMPLE_RATE = 2.4e6 # Sample rate in Hz
N_SAMPLES = 2**18 # Number of samples to capture

# Set signal processing parameters
FREQ_TOLERANCE = 5000 # Frequency tolerance in Hz
WINDOW_SIZE = 2**14 # Size of FFT window
NOISE_THRESHOLD = 10 # Threshold for noise reduction

# Initialize SDR device
sdr = rtl_sdr.RtlSdr()
sdr.center_freq = CENTER_FREQ
sdr.sample_rate = SAMPLE_RATE

# Capture data from SDR
samples = sdr.read_samples(N_SAMPLES)

# Perform FFT and extract hydrogen line signal
fft_data = np.fft.fftshift(np.fft.fft(samples, WINDOW_SIZE))
freqs = np.fft.fftshift(np.fft.fftfreq(WINDOW_SIZE, 1/SAMPLE_RATE))
signal_idx = np.argmin(np.abs(freqs - CENTER_FREQ))
signal_power = np.abs(fft_data[signal_idx])**2

# Perform noise reduction
noise_power = np.mean(np.abs(fft_data)**2)
if signal_power / noise_power > NOISE_THRESHOLD:
    signal_power -= noise_power

# Plot spectrum
plt.plot(freqs/1e6, 10*np.log10(np.abs(fft_data)**2))
plt.xlabel('Frequency (MHz)')
plt.ylabel('Power (dB)')
plt.show()
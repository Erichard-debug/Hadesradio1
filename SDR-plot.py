import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import astropy.units as u

class Analysis():
    def __init__(self):
        # Constants
        self.H_FREQUENCY = 1420405750
        self.C_SPEED = 299792.458 # km/s
    
    
    # Returns the radial velocity and maximum SNR
    def getRadialVelocity(self, data, freqs):
        # Center around H-line
        # TODO Change to radial velocity instead of frequency
        min_index = (np.abs(np.array(freqs)-self.freqFromRadialVel(120))).argmin()
        max_index = (np.abs(np.array(freqs)-self.freqFromRadialVel(-120))).argmin()

        SNR = np.amax(data[min_index:max_index])
        #Get index of max SNR
        index = np.where(data==SNR)[0][0]
        radial_vel = self.radialVelFromFreq(freqs[index])

        return np.round(SNR, 2), np.round(radial_vel, 2)
    

    # Returns radial velocity from frequency
    def radialVelFromFreq(self, freq):
        H_freq = u.doppler_radio(self.H_FREQUENCY*u.Hz)
        measured = freq*u.Hz
        v_doppler = measured.to(u.km/u.s,equivalencies=H_freq)
        
        return v_doppler.value
    

    # Returns frequency from radial velocity
    def freqFromRadialVel(self, radial_vel):
        H_freq = u.doppler_radio(self.H_FREQUENCY*u.Hz)
        measured = radial_vel*u.km/u.s
        freq = measured.to(u.Hz,equivalencies=H_freq)
        
        return freq.value

ANALYSIS = Analysis()

def spectrumGrid(ax, title, data_file_path, Y_MIN, Y_MAX):
    # Load data from the text file
    data = np.loadtxt(data_file_path, skiprows=1, delimiter=None, dtype=str)

    # Convert the loaded data to float
    frequency = data[:, 0].astype(float)
    relative_intensity_dB = data[:, 1].astype(float)

    start_freq = frequency[0]
    stop_freq = frequency[-1]

    ax.plot(frequency, relative_intensity_dB, color='g', label='Observed data')

    # Plots theoretical H-line frequency
    ax.axvline(x=ANALYSIS.H_FREQUENCY, color='r', linestyle=':', linewidth=2, label='Theoretical frequency')

    # Sets axis labels and adds legend & grid
    ylabel = 'Signal to noise ratio (SNR) / dB'
    xlabel = 'Frequency / MHz'  # Assuming frequency is in MHz
    title = title

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.set(xlim=[start_freq, stop_freq])
    ax.legend(prop={'size': 10}, loc=1)
    ax.grid()

    # Adds y-axis interval if supplied in config.txt
    if 0.0 == Y_MIN == Y_MAX:
        ax.autoscale(enable=True, axis='y')
    else:
        ax.set(ylim=[Y_MIN, Y_MAX])

    # Adds top x-axis for radial velocity
    radial_vel = ax.secondary_xaxis('top', functions=(ANALYSIS.radialVelFromFreq, ANALYSIS.freqFromRadialVel))
    radial_vel.set_xlabel(r'Radial velocity / $\frac{km}{s}$')


# Example usage:
fig, ax = plt.subplots()
spectrumGrid(ax, 'Mounted Parabolic Build', r'SDRTextFiles\para2.txt', 0, 0.0001)
plt.show()

import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np

freq_range = [300, 1100]

FREQ = np.arange(freq_range[0], freq_range[1], 1)


def frequency_response(c, r1, r2):
    Vout = [-r2/(c*(r1*r2+r1*r1)), 0]
    Vin = [1, 3/(c*(r1+r2)), 1/((c*c)*(r1*r2+r1*r1))]

    w, h = sig.freqresp((Vout, Vin), 2*np.pi*FREQ)

    return w, 20*np.log10(np.abs(h))


center_freq = []


def plot(c, r1, r2):
    mag = np.array(frequency_response(c, r1, r2)[1])
    max_index = np.where(mag == max(mag))[0][0]
    half_power = np.round(max(mag)-3, 1)
    bandwidth = np.where(np.round(mag, 1) == half_power)[0]+freq_range[0]
    print(bandwidth)
    plt.plot(FREQ, mag)
    plt.scatter(max_index+freq_range[0], mag[max_index])
    center_freq.append("Center: " + str(max_index+freq_range[0]) + "Hz")


y_range = [25, 50]
x_axis = np.arange(freq_range[0], freq_range[1]+1, 100)
y_axis = np.arange(y_range[0], y_range[1]+1, 2)

plot(.01e-6, 1200, 560e3)
plot(.01e-6, 1200, 510e3)
plot(.01e-6, 1200, 610e3)

legend = plt.legend(["R2 = 560K", center_freq[0], "R2 = 510K",
                     center_freq[1], "R2 = 610K", center_freq[2]])
legend.fontsize = 16
plt.ylim(y_range)
plt.xticks(x_axis)
plt.yticks(y_axis)
plt.title("Ideal Frequency Response of Bandpass Filters",
          fontdict={'size': 14})
plt.xlabel("Frequency (Hz)", fontdict={'size': 14})
plt.ylabel("Magnitude (dB)", fontdict={'size': 14})
plt.show()

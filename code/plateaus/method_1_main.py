from data_class import Data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r'~/Documents/Code/180F/data/180F_Voltage_Setup-Sheet1.csv')

peaks = [1.401, 1.35, 1.451, 1.401, 1.449]
scintillator_array = np.linspace(1, 5, 5)
d = Data(data=data)
q = (1 - 0.6827) / 2
for i in scintillator_array:
    d.set_scint_number(i)

    df = d.get_scint_data()

    voltage = df["V"]
    rate = df["rate"] # also the y-axis
    mean_rate = np.mean(rate, axis=0)
    
    error_bars = d.get_chi2_errors(q, rate)

    title = "Scintillator {}".format(int(i))
    print(i)
    d.plot_data(voltage, rate, peaks[int(i-1)], error_bars, title=title, log=True)
    
    #plt.savefig("~/Documents/Code/180F/data/plateaus/scint_{}.jpg".format(int(i)))

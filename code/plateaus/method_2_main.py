from data_class import Data
import numpy as np
import pandas as pd

data = pd.read_csv(r'~/Documents/Code/180F/data/180F_Voltage_Setup-Sheet2.csv')

q = (1 - 0.6827)
scintillator_array = np.linspace(1, 5, 5)
peaks = [1.499, 1.408, 1.381, 1.369, 1.542]

d = Data(data=data)
for i in scintillator_array:

    # setting up
    d.set_scint_number(i)
    df = d.get_scint_data()

    # rates
    three_counts_col = d.get_three_counts_col()
    two_counts_col = d.get_two_counts_col()
    three_counts_rate = df["{}".format(three_counts_col)]
    two_counts_rate = df["{}".format(two_counts_col)]

    # plotting
    voltage = df["V{}".format(int(i))] # x-axis
    ratio = df["ratio.1"] # y-axis
    error_bars = d.get_binomial_errors(q, two_counts_rate, three_counts_rate, ratio)

    title = "V{} vs {}".format(int(i), three_counts_col)
    y_label = "Ratio ({} / {})".format(three_counts_col, two_counts_col)
    d.plot_data(voltage, ratio, peaks[int(i-1)],
                error_bars, 
                title=title, 
                error=True, log=False, 
                y_label=y_label)

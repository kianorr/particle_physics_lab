import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Data():
    def __init__(self, data : pd.DataFrame, scint_number : int = None):
        '''Constructor for Data class.
        
        Parameters
        ----------
        `data`: <class 'pandas.core.frame.DataFrame'>
            DataFrame of original data.
        '''

        #assert type(data) == pd.DataFrame, "Data is a pandas dataframe"

        self.data = data
        if scint_number != None:
            self.scint_number = scint_number
    
    def set_data(self, data : pd.DataFrame) -> None:
        '''Setter for self.data.'''
        self.data = data
    
    def set_scint_number(self, scint_number : int) -> None:
        '''Setter for scint_number.'''
        self.scint_number = scint_number

    def get_data(self) -> pd.DataFrame:
        '''Getter for self.data.'''
        return self.data
    
    def get_scint_number(self) -> int:
        '''Getter for self.scint_number.'''
        return self.scint_number

    def get_three_counts_col(self) -> str:
        '''Chooses the correct name of the column for the three coincidences.'''

        column_name = {
            1: "C1C2C3",
            2: "C1C2C3",
            3: "C1C2C3",
            4: "C2C3C4",
            5: "C2C3C5"
        }

        return column_name[self.scint_number]
    
    def get_two_counts_col(self) -> str:
        '''Chooses the correct name of the column for the three coincidences.'''
        
        column_names = {
            1: "C2C3",
            4: "C2C3",
            5: "C2C3",
            2: "C1C3",
            3: "C1C2"
        }
        
        return column_names[self.scint_number]
    
    def get_scint_data(self) -> pd.DataFrame:
        '''Splits up data by scintillator number.

        Parameters
        ----------
        `scint_number`: <int>
            The scintillator (referenced by a number) on which the voltage was varied.
        
        Returns
        -------
        `scintillator_data`: <class 'pandas.core.frame.DataFrame'>
            DataFrame for a specific scintillator with varying voltage.
        '''
        scint_data = self.data[self.data["Scintillator"]==self.scint_number]
        scint_data = scint_data.dropna(axis="columns")
        return scint_data

    def get_chi2_errors(self, q, rate) -> np.ndarray:
        '''Gets errors with chi squared for error bars.

        Parameters
        ----------
        `q`: <int>
        `rate`: <class 'pandas.core.series.Series'>
            The number of counts. Any array-type is good.

        Returns
        -------
        `errors`: <class 'numpy.ndarray'>
            Any (2, n) array for plotting.
        
        '''
        low = abs(rate - scipy.stats.chi2.ppf(q, 2 * rate) / 2)
        high = abs(rate - scipy.stats.chi2.ppf(1 - q, 2 * rate + 1) / 2)
        errors = np.vstack([low, high])
        return errors

    def get_binomial_errors(self, q, trials, expected_succ, ratio) -> np.ndarray:
        '''https://gist.github.com/DavidWalz/8538435
        Clopper Pearson intervals. Expected successes are three coincidences and the trials are the
        two coincidences.
        
        Parameters
        ----------
        `q`: <int>
        `expected_succ`: any array data type
            three coincidences.
        `trials`: any array data type
            two coincidences.
        `ratio`: any array data type
            three coincidences / two coincidencecs
        '''
        low = scipy.stats.beta.ppf(q / 2, expected_succ, trials - expected_succ + 1) - ratio
        high = ratio - scipy.stats.beta.ppf(1 - q / 2, expected_succ + 1, trials - expected_succ)
        errors = np.vstack([low, high])
        return errors
        
    def plot_data(self, x, y, peak, error_bars=None, title="title", y_label="Rate (log)", x_label="Voltage", log=True, error=True):
        '''Plots the data with error bars.
        
        Parameters
        ----------
        `x`: <class 'pandas.core.series.Series'>
        `y`: <class 'pandas.core.series.Series'>
        `error_bars`: <class 'numpy.ndarray'>
        `scint_number`: <int>
        `y_label`: <string>
        `x_label`: <string>
        `log`: <boolean>
            `True` for log and `False` for not log plot.
        '''
        if log == True:
            plt.yscale("log")
        if error == True:
            plt.errorbar(x, y, yerr=error_bars, fmt='None', capsize=3)
        plt.scatter(x, y)
        plt.ylabel("{}".format(y_label))
        plt.xlabel("{}".format(x_label))
        plt.title(title)
        plt.axvline(x=peak, linestyle='--', color='red')
        plt.show()

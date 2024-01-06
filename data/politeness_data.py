target_path = "datao/"
import requests
import os
import pathlib
import polars as pl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class PolitenessData():
    def __init__(self, data_url, target_path, data_file):
        """Download, preprocess, and plot politeness data from Bodo Winter

        Parameters
        ----------
        data_url : str 
            Url from where to download the data set.
        target_path : str
            local working directory where data should be stored.
        data_file : str
            name of file to which data should be saved.

        Returns
        -------
        cwd : str
            Information about the current working directory.
        summary_stats : DataFrame
            Summary statistics of the politeness data.
        plot : plt.plot
            Plot of the politeness data.

        """
        self.target_path = target_path
        self.data_url = data_url
        self.data_file = data_file
        
    def __call__(self):

        # set current working directory   
        self.set_cwd(self.target_path)
        # download data set from specified url
        self.download_data(self.data_url, file_name = self.data_file)
        # read and preprocess data set
        df, summary_stats = self.data_preprocessed(self.data_file)
        # show summary statistics
        print(summary_stats)
        # plot data
        self.plot_data(df)
  
    def set_cwd(self, target_path):
        """Set current working directory to desired local path

        Parameters
        ----------
        target_path : str
            local path that should be used as current working directory.

        Returns
        -------
        current_working_directory : str
            Prints current working directory.

        """
        # set the current working directory 
        os.chdir(target_path)
        
        # get current working directory
        current_wd = pathlib.Path.cwd()
        # check whether current working directory is indeed correct
        # if not: returns an error
        assert  current_wd == target_path, "Current working directory does not match with target directory"
        return print("current working directory:", current_wd)
    
    def download_data(self, data_url, file_name):
        """Download data from url

        Parameters
        ----------
        data_url : str
            URL from which data should be downloaded.
        file_name : str
            Name by which downloaded data file should be locally saved.

        Returns
        -------
        None.

        """
        # get data from url
        response = requests.get(data_url)
        with open(file_name, "wb") as file:
            file.write(response.content)
            
    # install pyarrow via pip install pyarrow
    def data_preprocessed(self, data_file):
        """Read and preprocess data 

        Parameters
        ----------
        data_file : str
            name of locally saved data file.

        Returns
        -------
        df_joined : polars.DataFrame
            Preprocessed data set with 84 observations and 6 variables (subject, 
            gender, scenario, attitude, frequency, mean_pitch).
        summaries : polars.DataFrame
            Mean pitch value grouped by attitude (informel, polite) and gender 
            (female, male).

        """
        # read data
        df = pl.from_pandas(pd.read_csv(data_file))
        # compute mean pitch values, grouped by gender and attitude
        summaries = df.group_by("attitude", "gender").agg(
            mean_pitch = pl.col("frequency").mean()
            )
        # join summaries and df columns together
        df_joined = df.join(summaries, on = ["gender", "attitude"], how = "inner")
        # relable attitude values
        df_joined = df_joined.with_columns(pl.lit(df["attitude"].map_dict({"pol": "polite", "inf": "informal"})).alias("attitude"))

        return (df_joined, summaries)
    
    def plot_data(self, df):
        """Scatterplot showing the relation between pitch in Hz and gender and 
        attitude.

        Parameters
        ----------
        df : polars.DataFrame
            Preprocessed data set with 84 observations and 6 variables (subject, 
            gender, scenario, attitude, frequency, mean_pitch).

        Returns
        -------
        matplotlib.plot

        """
        # create color sequence for grouping variable 
        # (to be passed into plot)
        cols = np.where(df["attitude"] == "polite", "lightblue", "orange")
        
        # initialie new plot
        fig, axs = plt.subplots(constrained_layout = True)
        # plot mean values
        axs.scatter(df["gender"],df["mean_pitch"], c = cols,edgecolors='black')
        # plot additionally individual observations
        sns.swarmplot(data = df,
                    x = "gender", y = "frequency", 
                    hue = "attitude",
                    alpha = 0.4, ax=axs)
        # relable x-axis
        axs.set_xticklabels(labels = ["Female", "Male"])
        axs.set_ylabel("pitch in Hz")
        plt.show()
       
    
# here we use pathlib.PureWindowsPath s.t. we don't need to care about
# direction of backslashes
target_path = pathlib.PureWindowsPath(r"C:\Users\Mustafa\Desktop\moustafa-project") 
# data set
data_url = "http://www.bodowinter.com/tutorial/politeness_data.csv"    
data_file = "pitch_data.csv"

# initialize class and create a new instance
pol_data = PolitenessData(data_url, target_path, data_file)

help(PolitenessData)
dir(PolitenessData)
# set working directory
pol_data.set_cwd(target_path)

# download data set
pol_data.download_data(data_url, data_file)

# preprocess data set
df, df_sum = pol_data.data_preprocessed(data_file)

# plot data 
pol_data.plot_data(df)


class DownloadData:
    def __init__(self):
        # Implement the initialization for DownloadData
        pass
    
    def set_working_directory(self):
        # Add code to set the working directory
        pass
    
    def download_dataset(self):
        # Add code to download the dataset
        pass
    
    
class PolitenessData:
    def __init__(self):
        # Implement the initialization for PolitenessData
        pass
    
    def preprocess_data(self):
        # Add code to preprocess the data
        pass
    
    def plot_data(self):
        # Add code to plot the data
        pass


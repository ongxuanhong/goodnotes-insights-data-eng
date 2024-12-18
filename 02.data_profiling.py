import pandas as pd
from ydata_profiling import ProfileReport


def profiling_data(filename):
    pd_data = pd.read_csv(f"data/{filename}.csv")

    a = ProfileReport(pd_data, title=f"Profiling Report: {filename}")
    a.to_file(f"profiles/{filename}.html")


profiling_data(filename="user_metadata_sample")
profiling_data(filename="user_interactions_sample")

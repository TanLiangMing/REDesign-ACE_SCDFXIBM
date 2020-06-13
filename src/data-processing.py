import numpy as np
import pandas as pd
import os

def loadTimeSeriesData():
    """Loads the time series data from an excel file"""
    return data

def processTimeSeriesData(data, window_length):
    """Uses a sliding window to process the time series data into datapoints"""
    return datapoints

def saveDataPoints(datapoints, window_length):
    """Saves the datapoints into the output file"""
    return

def main():
    time_series_data = loadTimeSeriesData()
    window = [5, 10, 30, 60]
    for window in windows:
        datapoints = processTimeSeriesData(time_series_data, window)
        saveDataPoints(datapoints, window)

if __name__ == "__main__":
    main()
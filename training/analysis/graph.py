#Creates the graphs for the analysis
__author__ = "Hamnah Qureshi"


#Imports
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib import figure

#Global Variables
fig, axis = plt.subplots(1,2)  #Subplot of two graphs


#Creates an histogram with values provided
def histogram (data, binWidth, xLabel, yLabel, xMax, yMax, title, yAxis) ->None:
    axis[yAxis].hist(data, bins = range(min(data), max(data)+ binWidth, binWidth), color='red', edgecolor='black', alpha=0.5, rwidth=0.8)
    axis[yAxis].axis([0,xMax,1,yMax])
    axis[yAxis].set_xlabel("Number of "+ xLabel)
    axis[yAxis].set_ylabel("Number of " + yLabel)
    axis[yAxis].set_title(title, fontsize=8)
    


#Plots the graph and shows a text analysis of the data
def plot(text):
    plt.figtext(0.8,0.55, text, wrap = True, ha= "center",fontsize=8, bbox= {"facecolor": "green", "alpha": 0.5, "pad":3})
    plt.savefig("collection/analysis/graphs/data analysis.png")
    plt.subplots_adjust(bottom=0.75)
    plt.close()






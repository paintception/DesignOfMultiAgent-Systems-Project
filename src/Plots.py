from matplotlib import pyplot as pyplot
from matplotlib import pylab as pylab
from scipy import stats as stats
import numpy as np

def plot_averages_with_sdvs(Data, x_label, y_label, Title):
	'''
	Data is a two dimensional array ith the data arrays for every class.
	Title is the tile of the plot as string
	y_lable is y lable as string
	x_lable tupple of strings for y lable same length as data
	'''
	x_mean =[] 
	x_std = []
	width = 0.35
	
	for e in Data:
		x_mean.append(np.mean(e))
		x_std.append(np.std(e))

	ind = np.arange(len(x_mean)) 
	pyplot.figure()
	pyplot.title(Title)
	for i in range(len(x_mean)):
		pyplot.bar(ind[i],x_mean[i],width,align='center',yerr=x_std[i],ecolor='k')
	pyplot.ylabel(y_label)
	pyplot.xticks(ind, x_label) 
	pyplot.show()

def plot_regression_line_with_pointcloud(Data,x_labe, y_lable, Title, Classes):

	fig = pyplot.figure()
	ax1 = fig.add_subplot(121)
	axl.title(Title)	

	data_x, data_y = zip(*Data[0])
	axl.scatter(data_x, data_y)
	
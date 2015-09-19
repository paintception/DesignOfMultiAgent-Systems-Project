from Agent import Agent
from Grid import Grid
import math
import numpy

class Memory():


	def __init__(self, width, height):
		self.jams = numpy.zeros((height,width)) 
	
	def addJam(self, x, y velosity ):
		self.jams[y][x]=velosity

	def getGridPoint(self ,x ,y):
		return self.jams[y][x]
		

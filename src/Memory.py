from Agent import Agent
from Grid import Grid
import math
import numpy

class Memory():


	def __init__(self, width, height):
		self.jamsY = numpy.zeros((height-1,width))
		self.jamsX = numpy.zeros((height,width-1)) 
	
	def addJam(self, x1, y1, x2, y2, velosity ):
		if x1!=x2 and y1!=y2
			print "nop"		
		elif x1 < x2:
			self.jamsX[y1][x1]=velosity
		elif x2 < x1:
			self.jamsX[y1][x1]=velosity
		elif y1 < y2:
			self.jamsY[y1][x1]=velosity
		elif y2 < y1:
			self.jamsY[y2][x1]=velosity
		else
			print "fuck you"

	def getGridPoint(self ,x1 ,y1, x2, y2):
		if x1!=x2 and y1!=y2
			print "nop"
			return 0			
		elif x1 < x2:
			return self.jamsX[y1][x1]
		elif x2 < x1:
			return self.jamsX[y1][x1]
		elif y1 < y2:
			return self.jamsY[y1][x1]
		elif y2 < y1:
			return self.jamsY[y2][x1]
		else
			print "fuck you"
			return 0
		
		

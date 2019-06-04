#! /usr/bin/env python


# INSTRUCTIONS:
#
# Use left mouse to zoom in, and right mouse to zoom out.
# Use arrow keys to navigate graph. Use 'c' key to center graph.
# Use 'm' key to print mouse location.

#~~~~~~~~~~~~~~~~~~~USER-DEFINED VARIABLES~~~~~~~~~~~~~~~~~~~#
width = 750		# The width and depth of the
depth = 750		# graph window in pixels.

xmin = -10		# These are the window range variables.
xmax = 10		# They define the minimum and maximum X and
ymin = -10		# Y values that the graphing program
ymax = 10		# window displays.

grid = 2		# The number of units between gridlines
				# (Only functional if autoG = False).

autoG = True	# Automatically change grid resolution
				# depending on graph resolution.

# The functions to graph. Use Python math code.

functions = [
	"x**2",
]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def mouseHandle(button, point, mode, g):
	if mode == 0:
		if button == 1: g.zoom(0.833, point); redrawGraph(g)
		elif button == 3: g.zoom(1.2, point); redrawGraph(g)
	elif mode == 1:
		if button == 1: g.zoom(0.714, point); redrawGraph(g)
		elif button == 3: g.zoom(1.4, point); redrawGraph(g)

def keyHandle(key, mode, g):
	if mode == 0:	
		if key == pygame.K_UP: g.wShift(shift*g.yres, (0, 1)); redrawGraph(g)
		elif key == pygame.K_DOWN: g.wShift(shift*g.yres, (0, -1)); redrawGraph(g)
		elif key == pygame.K_LEFT: g.wShift(shift*g.xres, (-1, 0)); redrawGraph(g)
		elif key == pygame.K_RIGHT: g.wShift(shift*g.xres, (1, 0)); redrawGraph(g)
		elif key == pygame.K_c: g.setWindow(-g.xres/2, g.xres/2, -g.yres/2, g.yres/2); redrawGraph(g)
		elif key == pygame.K_m: g.printMouse(pygame.mouse.get_pos())
	if mode == 1:
		if key == pygame.K_UP: g.wShift(shift*2*g.yres, (0, 1)); redrawGraph(g)
		elif key == pygame.K_DOWN: g.wShift(shift*2*g.yres, (0, -1)); redrawGraph(g)
		elif key == pygame.K_LEFT: g.wShift(shift*2*g.xres, (-1, 0)); redrawGraph(g)
		elif key == pygame.K_RIGHT: g.wShift(shift*2*g.xres, (1, 0)); redrawGraph(g)

def redrawGraph(g):
	g.redraw()
	pygame.display.flip()

class Graph:
	def __init__(self, surf):
		self.surf = surf
		self.xmin = 0.0
		self.xmax = 0.0
		self.ymin = 0.0
		self.ymax = 0.0
		self.xres = 0.0
		self.yres = 0.0
		self.grid = 0.0
		self.xpix = 0.0
		self.ypix = 0.0
		self.bgCol = 0, 0, 0
		self.gridCol = 100, 0, 0
		self.axesCol = 255, 0, 0
		#self.fcol = 0, 0, 255
	
	def setWindow(self, x1, x2, y1, y2):
		self.xmin = x1
		self.xmax = x2
		self.ymin = y1
		self.ymax = y2
		self.xres = float(x2) - x1
		self.yres = float(y2) - y1
		self.xpix = float(width)/self.xres
		self.ypix = float(depth)/self.yres
		#if autoG == True: self.grid = int(ceil(2**round(log(self.xres*autoGRes, 2))))
		if autoG == True:
			cl = [1.0, 2.5, 5.0]
			self.grid = min([c*10**ceil(log(self.xres*autoGMR/c, 10)) for c in cl])
			if self.grid < 1.0: self.grid = 1.0
	
	def setGrid(self, g):
		self.grid = g
	
	def graphToScreen(self, point):
		return ((point[0] - self.xmin)*self.xpix, (self.ymax - point[1])*self.ypix)
	
	def screenToGraph(self, point):
		return (point[0]/self.xpix + self.xmin, self.ymax - point[1]/self.ypix)
	
	def zoom(self, factor, point):
		x, y = self.screenToGraph(point)
		#self.setWindow(x - self.xres/2*factor, x + self.xres/2*factor, y - self.yres/2*factor, y + self.yres/2*factor)
		self.setWindow(x - (x - self.xmin)*factor, x + (self.xmax - x)*factor, y - (y - self.ymin)*factor, y + (self.ymax - y)*factor)
	
	def wShift(self, units, dir):
		self.setWindow(self.xmin + dir[0]*units, self.xmax + dir[0]*units, self.ymin + dir[1]*units, self.ymax + dir[1]*units)
	
	def printMouse(self, point):
		x, y = self.screenToGraph(point)
		x, y = round(x, 4), round(y, 4)
		print("Mouse at (%.4f, %.4f)" % (x, y))
	
	def drawGrid(self):
		xGpix = self.xpix*self.grid
		yGpix = self.ypix*self.grid
		xadj = int((float(-self.xmin)/self.grid - floor(float(-self.xmin)/self.grid))*xGpix)
		yadj = int((float(self.ymax)/self.grid - floor(float(self.ymax)/self.grid))*yGpix)
		for i in range(int(self.xres/self.grid) + 1):
			x = int(xGpix*i) + xadj
			pygame.draw.line(self.surf, self.gridCol, (x, 0), (x, depth))
		for i in range(int(self.yres/self.grid) + 1):
			y = int(yGpix*i) + yadj
			pygame.draw.line(self.surf, self.gridCol, (0, y), (width, y))
		if self.ymin <= 0.0 and self.ymax >= 0.0:
			y0 = int(self.ymax*self.ypix)
			pygame.draw.line(self.surf, self.axesCol, (0, y0), (width, y0))
		if self.xmin <= 0.0 and self.xmax >= 0.0:
			x0 = int(-self.xmin*self.xpix)
			pygame.draw.line(self.surf, self.axesCol, (x0, 0), (x0, depth))
	
	def drawGraph(self, fIndex):
		screeny = 0
		oldy = None
		f = functions[fIndex]
		fc = fcol[fIndex]
		
		for screenx in range(width + 1):
			x = screenx/self.xpix + self.xmin
			
			try:
				y = eval(f)
			except:
				oldy = None
				continue
			
			screeny = (self.ymax - y)*self.ypix
			if oldy != None:
				if (depth - min(screeny, oldy))*max(screeny, oldy) > 0:
					pygame.draw.line(self.surf, fc, (screenx - 1, oldy), (screenx, screeny))
			oldy = screeny
	
	def redraw(self):
		self.surf.fill(self.bgCol)
		self.drawGrid()
		for f in range(len(functions)):
			self.drawGraph(f)

import pygame
from math import *
import random
pygame.init()

screen = pygame.display.set_mode((width, depth))

autoGMR = 0.1
shift = 0.05

# function color array

fcol = [
	(0, 0, 255),
	(0, 255, 0),
	(255, 255, 0)
]

# key and mouse press time dicts

keyPressT = {

pygame.K_UP: (-1, 0),
pygame.K_DOWN: (-1, 0),
pygame.K_LEFT: (-1, 0),
pygame.K_RIGHT: (-1, 0)

}

mousePressT = {

1: (-1, 0),
3: (-1, 0)

}

#mhandles = 0
#khandles = 0

graph = Graph(screen)
graph.setWindow(xmin, xmax, ymin, ymax)
if autoG == False: graph.setGrid(grid)
redrawGraph(graph)

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouseHandle(event.button, event.pos, 0, graph)
			if mousePressT.has_key(event.button):
				mousePressT[event.button] = (pygame.time.get_ticks(), 0)
		elif event.type == pygame.MOUSEBUTTONUP:
			if mousePressT.has_key(event.button):
				mousePressT[event.button] = (-1, 0)
				#mhandles = 0
		elif event.type == pygame.KEYDOWN:
			keyHandle(event.key, 0, graph)
			if keyPressT.has_key(event.key):
				keyPressT[event.key] = (pygame.time.get_ticks(), 0)
		elif event.type == pygame.KEYUP:
			if keyPressT.has_key(event.key):
				keyPressT[event.key] = (-1, 0)
				#khandles = 0
	
	for mbutton, t in mousePressT.iteritems():
		curT = pygame.time.get_ticks()
		if t[0] != -1 and (curT - t[0]) >= 500 and (curT - t[0] - 500) >= t[1]*80:
			mouseHandle(mbutton, pygame.mouse.get_pos(), 1, graph)
			mousePressT[mbutton] = (t[0], t[1] + 1)
	
	for key, t in keyPressT.iteritems():
		curT = pygame.time.get_ticks()
		if t[0] != -1 and (curT - t[0]) >= 500 and (curT - t[0] - 500) >= t[1]*80:
			keyHandle(key, 1, graph)
			keyPressT[key] = (t[0], t[1] + 1)

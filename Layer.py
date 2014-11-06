# -*- coding: utf-8 -*-

import numpy 

class Layer(object):
#    def __init__(self, xySize, fSize, xyStart, xySpace, inputLayers=[]):
    def __init__(self, xySize, fSize, xyStart, xySpace,inputLayers=[]):
        #Layer.__init__(self,  xySize, fSize, xyStart, xySpace, inputLayers)
        self.__xySize = xySize
        self.__fSize = fSize
        #self.__level = level
        self.xyStart = xyStart
        self.xySpace = xySpace
        self.cArray = None
        self.inputLayers = inputLayers
        #print len(self.inputLayers)
        self.array = numpy.zeros((self.__fSize,self.__xySize,self.__xySize))
        #print self.array[0,0,0]
        #print xySize
    def SetLayer(self,mxArray):
        #print mxArray
        #self.array[0]=mxArray
        #print self.array[0,2,0]
        #print self.array.shape
        for xi in range(self.__xySize):
            for yi in range(self.__xySize):
                self.array[0,xi,yi]=mxArray[xi,yi]
        #print self.array[0,5,5]

        #print self.array.shape
        #return self.array
                
                #self.inputLayers.append(inputLayer)
        #print self.inputLayers


    def set(self, ipos, f, val):
        xi,yi=ipos
        self.array[f,xi,yi]=val
    def get(self,ipos,f):
        #print self.array
        #print f,ipos
        xi,yi=ipos
        #print self.array
        #print self.array[f,5,5]
        return self.array[f,xi,yi]
    def InputArray(self):
        return self.array
    def xyCenter(self, xyi):
        return (self.xCenter(xyi[0]), self.yCenter(xyi[1]))
    def xCenter(self, xi):
        return self.xyStart + (xi*self.xySpace)
    def yCenter(self, yi):
        return self.xyStart + (yi*self.xySpace)
        
    def getXRFNear(self, c, n):
        i1,i2,j1,j2 = self.__getRFNear(self.__xySize, self.xyStart, self.xySpace, c, n)
        #print self.xSize()
        return ((i1,i2), (i1==j1) and (i2==j2))
    def getYRFNear(self, c, n):
        i1,i2,j1,j2 = self.__getRFNear(self.__xySize, self.xyStart, self.xySpace, c, n)
        return ((i1,i2), (i1==j1) and (i2==j2))
    def __getRFNear(self, t, s, d, c, n):
        dd = 1.0 / d
        j1 = int(numpy.ceil((c - s) * dd - 0.5 * n - 0.001))
        j2 = j1 + n - 1
        i1 = min(max(j1, 0), t)
        #print t
        #print "aa"
        i2 = min(max(j2,-1), t-1)
        return i1,i2,j1,j2
    def getXRFDist(self, c, r):
        i1,i2,j1,j2 = self.__getRFDist(self.__xySize, self.xyStart, self.xySpace, c, r)
        return ((i1,i2), (i1==j1) and (i2==j2))
    def getYRFDist(self, c, r):
        i1,i2,j1,j2 = self.__getRFDist(self.__xySize, self.xyStart, self.xySpace, c, r)
        return ((i1,i2), (i1==j1) and (i2==j2))
    def __getRFDist(self, t, s, d, c, r):
        dd = 1.0 / d
        j1 = int(numpy.ceil( (c - r - s) * dd - 0.001))
        j2 = int(numpy.floor((c + r - s) * dd + 0.001))
        i1 = min(max(j1, 0), t)
        i2 = min(max(j2,-1), t-1)
        return i1,i2,j1,j2
    def GetLayer(self):
        return self.array


    def xySize(self):
        return self.__xySize
    def xSize(self):
        return self.__xySize
    def ySize(self):
        return self.__xySize
    def fSize(self):
        return self.__fSize
    

# -*- coding: utf-8 -*-

"""
This file contains the definition of a single data layer within
a given hierarchical level within an HMAX network.

An HMAX network is designed to take an input image and produce multiple
resized versions (scales) of the image.  The intent is that a range of
image sizes will help the algorithm become exposed to a greater range
of object sizes.  Since we keep the Gabor filter size fixed (at say 9x9),
as we decrease the image resolution the Gabor filter is effectively 
covering a larger and larger area of the image.  In this way we can
detect orientated lines at a range of sizes from rather small to
rather large.

A single layer then contains a set of data usually to represent a given
size scaling.  By having multiple layers we can store multiple image scales
at once and process then in parallel.  As we ascend the hierarchy we slowly
combine the scale layers by selecting the best responses between 2 neighboring
scales resulting in an overall best response across many sizes.

Layers have a concept of both discrete-space and what we call retinal-space.
The discrete space is simply the actual indicies corresponding to a numpy 2d
matrix that is storing the actual layer values (i.e. the pixel values for
the image).  While retinal-space is a real-valued global space, where (0.0,0.0)
indicate the center of the image and this location is consistent across all
hierarchical levels despite that each level will have discrete matricies
of differing dimensions.  Using the retinal-space we have a way of ensuring
accurate comparisons of locations across different layers in different levels.

Layers are also given an ability to render themselves to a wx canvas image.
The default rendering simply maps the layer values to a 0-255 range and
colors the cells between black and white to show the range of values present.

However some layers can implement more elaborate rendering schemes to help
visualize more specific results.  For example the C2 SVM can render a bar
graph depicting its classification results. 
"""


import numpy

class Layer(object)
    def __init__(self, xySize, fSize, xyStart, xySpace,inputLayers=[]
    """
    Allocate a new layer of size [(xySize) by fSize].  The remaining four 
    parameters determine the (X, Y) grid positions in the common, 
    real-valued coordinate system.  xyStart is the position of XY index 0, 
    and xySpace determines the spacing between adjacent grid points along XY.  
    @param xySize: (x,y) integer tuple of size for this layer. 
    @param fSize: integer describing how many features (i.e. orientations, 
    templates, variations) this layer will contain.  Each feature is basically
    representing a different way to populate the values of the layer.
    @param xyStart: (xr,yr) real-value tuple mapping the upper-left (0,0) corner
    of the layer to its real-coordinate space equivalent.
    @param xySpace: (xs,ys) real-value tuple describing the spacing between
    layer cells in terms of real-coordinate space.
    @param inputLayers: list of Layers that are connected as the inputs to
    this current layer.
    """
        self.__xySize = xySize
        self.__fSize = fSize
        self.xyStart = xyStart
        self.xySpace = xySpace
        self.cArray = None
        self.inputLayers = inputLayers
        self.array = numpy.zeros((self.__fSize,self.__xySize,self.__xySize)
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
        """ 
    Assign the value 'val' into this layer's data matrix at location 
    ipos (x,y) in feature f. 
    """
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
 """
    Convert the input layer-space integer xy-coordinate into its
    equivalent in real-valued retinal space.  Since a layer space
    coordinate represents a cell in retinal-space, the returned
    value will represent the center point of that cell.
    @param xyi: tuple (x,y) of an integer xy-coordinate in layer-space.
    @return: tuple (rx,ry) of the real-valued xy-coordinate in retinal-space.
    """
        return (self.xCenter(xyi[0]), self.yCenter(xyi[1]))
    def xCenter(self, xi):
        return self.xyStart + (xi*self.xySpace)
    def yCenter(self, yi):
 """ 
    Convert the input layer-space integer y-coordinate into its
    equivalent in real-valued retinal space.  Since a layer space
    coordinate represents a cell in retinal-space, the returned
    value will represent the center point of that cell.
    @param xi: integer x-coordinate in layer-space.
    @return: equivalent real-valued x-coordinate in retinal-space.
    """
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
 """
    Similar to getXRFNear above, except instead of finding the N nearest 
    indices, we find all indices within distance R of C, both specified 
    in real-value retinal coordinates.  If any of the indices found are 
    invalid, the range in I1/I2 is truncated and the return value will 
    be false, otherwise we return true.
    @return: ((i1,i2), isOK)
    """
        i1,i2,j1,j2 = self.__getRFDist(self.__xySize, self.xyStart, self.xySpace, c, r)
        return ((i1,i2), (i1==j1) and (i2==j2))
    def getYRFDist(self, c, r):
"""
    Similar to getYRFNear above, except instead of finding the N nearest 
    indices, we find all indices within distance R of C, both specified 
    in real-value retinal coordinates.  If any of the indices found are 
    invalid, the range in I1/I2 is truncated and the return value will 
    be false, otherwise we return true.
    @return: ((i1,i2), isOK)
    """
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
    

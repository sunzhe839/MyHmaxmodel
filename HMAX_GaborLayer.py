# -*- coding: utf-8 -*-
#Applies a set of gabor filters at each position in a single image.
import numpy
from Filter_r4 import Filter

#import matplotlib.pyplot as plt

class GaborFilter(Filter):
    def __init__(self, yxCount, aspect, lamb, sigma, fCount):
        self.m_yxCount=yxCount
        self.m_fCount=fCount
        self.aspect=aspect
        self.lamb=lamb
        self.sigma=sigma



        #print numpy.pi
        #YXCOself,UNT - edge size of the filters in pixels.
        # ASPECT, LAMBDA, SIGMA - gabor filter parameters.
        # FCOUNT - number of different filters, i.e. the number of orientations.
        self.m_gabors=numpy.zeros([self.m_fCount,self.m_yxCount,self.m_yxCount])
        ptr=numpy.zeros([self.m_yxCount,self.m_yxCount])
        ptr_mul=numpy.zeros([self.m_yxCount,self.m_yxCount])
        #ptr=[]
        #print ptr
        #print m_yxCount,m_fCount
        m_mean=numpy.zeros(self.m_fCount)
        for f in range(self.m_fCount):
            #print f
            for j in range(self.m_yxCount):
                for i in range(self.m_yxCount):
                    
                    jj=0.5*(1-self.m_yxCount)+j
                    ii=0.5*(1-self.m_yxCount)+i
                    theta=f/self.m_fCount*numpy.pi
                    y=jj*numpy.sin(theta)+ii*numpy.cos(theta)
                    x=jj*numpy.cos(theta)-ii*numpy.sin(theta)
                    if numpy.sqrt(x*x+y*y) <= 0.5*self.m_yxCount:
                        e=numpy.exp(-(x*x+self.aspect*self.aspect*y*y))/(2.0*self.sigma*self.sigma)
                        e=e*numpy.cos(2.0*numpy.pi*x/self.lamb)
                    else:
                        e=0.0
                    #print e
                    ptr[j,i]=e
                    #print ptr
            #ptr=numpy.array(ptr)
                    ptr_mul[j,i]=e**2
            n=self.m_yxCount**2
            ptr_mean=numpy.mean(ptr)
            
            ptr_stdv=numpy.sqrt(numpy.sum(ptr_mul)-numpy.sum(ptr)**2/n)
            ff=0        
            for iy in range(self.m_yxCount):
                for jx in range(self.m_yxCount):
                    ptr[iy,jx]=(ptr[j,i]-ptr_mean)/ptr_stdv
                #ff=ff+1
                
            #print ptr
            #print ptr.shape
            self.m_gabors[f,:,:]=ptr
            #if f==0:
                #m_gabors[0]=ptr
    #            m_gabors=numpy.array(ptr)
            #e##lse:
                #m_gabors[f]=ptr
                #print m_gabors
            #ptr=[]
            #print m_gabors[2]
            #print ptr.shape
            #ptr=numpy.zeros(self.m_yxCount*self.m_yxCount)
        #return m_gabors

        #plt.plot(m_gabors[6])
        #plt.show()
        #print len(m_gabors)
        #plt.plot(m_gabors[10])
        #plt.show()
        #Normalize it have mean 0 and total energy1.
        #m_gabors=numpy.array(m_gabors) 
        #print len(self.m_gabors)
        #n=m_yxCount*m_yxCount



    def FCount(self):
        return self.m_fCount
        #print self.m_fCount
    def computeUnit(self,layerInputs,pos,f):

        cx,cy=pos
        layerInput = layerInputs[0]
        (xi1,xi2), xOK = layerInput.getXRFNear(cx, self.m_yxCount)
        if not xOK:
	        return 0
        (yi1,yi2), yOK = layerInput.getYRFNear(cy, self.m_yxCount)
        if not yOK:
	        return 0
        res=0.0
        lenc=0.0
        gabor = self.m_gabors[f,:,:]
        #print len(gabor)
        #print "bb"
        for xi in xrange(xi1, xi2+1):
            for yi in xrange(yi1, yi2+1):
                #print "cc"
                #print (xi-xi1),(yi-yi1)
                w = gabor[(xi-xi1),(yi-yi1)]
                #print xi,yi
                v = layerInput.get((xi,yi), 0)
                #print v
                res += w*v
                lenc += v*v
                #print res
                       
        res = abs(res)
        #print res,lenc         
        if lenc>0:
            res /=numpy.sqrt(lenc)
        #print res
        return res
        #print res
        #print "aa

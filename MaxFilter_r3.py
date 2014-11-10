#Performs a per-feature local maximum over position and scale in one or
# more input layers.
# SCOUNT - number of scales over which to pool.
# YXCOUNT - number of grid positions (in the largest scale) over which to pool.
from Filter_r4 import Filter
class MaxFilter(Filter):
    def __init__(self,sCount,yxCount):
        self.m_sCount  = sCount
        self.m_yxCount = yxCount
    
    def computeUnit(self,layerInputs,pos,f):
        #Re-express YXCOUNT as a distance in real-valued retinal coordinates.
        #inarray=layerInputs.InputArray()
        #layerInput=layerInputs[0]
        yr=layerInputs[0].xySpace*0.5*self.m_yxCount
        xr=layerInputs[0].xySpace*0.5*self.m_yxCount
    #Now for each input layer (i.e. each scale) perform a local max 
    #over position for feature F.
        xc,yc = pos
        res=0
        for s in xrange(self.m_sCount):
            #print s
            #print len(layerInputs)
            (xi1,xi2), xOK = layerInputs[s].getXRFDist(xc,xr)
            (yi1,yi2), yOK = layerInputs[s].getYRFDist(yc,yr)
            #xi=xi1
            #yi=yi1
            for xi in range(xi1,xi2+1):
                for yi in range(yi1,yi2+1):
                    v = layerInputs[s].get((xi,yi), f)
                    res = max(res, v)
        return res



#MaxFilter(2,10)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os, shutil
import scipy


class vector:
    def __init__(self,values) -> None:
        self.values = values

    def __len__(self):
        return len(self.values)
        
    def __sub__(self,other):
        if len(self.values) != len(other.values):
            return 'unable to perform subtraction'
        new_vector = []
        for i in range(len(self.values)):
            new_vector.append(self.values[i] - other.values[i])
        return vector(new_vector)


    def __add__(self,other):
        if len(self.values) != len(other.values):
            return 'unable to perform subtraction'
        new_vector = []
        for i in range(len(self.values)):
            new_vector.append(self.values[i] + other.values[i])
        return vector(new_vector)

    def __getitem__(self,i):
        return self.values[i]
    
    def __mul__(self, factor):
        scalar = 0
        if isinstance(factor,vector):
            if len(self.values) != len(factor.values):
                raise RuntimeError( 'unable to perform vector multiplication' )
            for i in range(len(self.values)):
                scalar += self.values[i] * factor.values[i]
                return scalar
        else:
            new_vector = []
            for i in range(len(self.values)):
                new_vector.append(self.values[i] * factor)
            return vector(new_vector)

    def __rmul__(self,factor):
        return self.__mul__(factor)

    def slope(self):
        return self.values[0]/self.values[1]

    def getOrthogonalVector(self):
        m = self.slope()
        deltaY = 1
        deltaX = -1*m*deltaY
        return vector([deltaX,deltaY])

    
    def vectorLength(self):
        sumSquare = 0 
        for i in range(len(self.values)):
            sumSquare += (self.values[i])**2
        return np.sqrt(sumSquare)



currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, 'sizeDistribution.xlsx')

df = pd.read_excel(dataPath, header=1)
sizeDistribution = []
volumeFrequency = []
accumulatedVolumeFrequency = []
for i in range(len(df['Größe (μm)'])):
    sizeDistribution.append(df['Größe (μm)'][i])
    volumeFrequency.append(df['% Volumen In'][i])
    accumulatedVolumeFrequency.append(df[df.columns[2]][i])

for i in range(len(accumulatedVolumeFrequency)):
        if accumulatedVolumeFrequency[i] == 100:
            xmax = sizeDistribution[i+4]
            break
for i in range(len(accumulatedVolumeFrequency)):
        if accumulatedVolumeFrequency[i] != 0:
            xmin = sizeDistribution[i-4]
            break

def computeLognormDistribution(µ,sigma):
    lognormDistribution = []
    for i in range(len(sizeDistribution)):
        x = (1./(sigma * sizeDistribution[i] * np.sqrt(2* np.pi))) * np.exp(-((np.log(sizeDistribution[i])-µ)**2)/(2*sigma**2))
        lognormDistribution.append(x)

    lognormDistribution = np.array(lognormDistribution)
    lognormDistribution *= 100./np.sum(lognormDistribution)

    return lognormDistribution



def getDeviation(argIn, imageCounter=0, drawImage= False):

    µ = argIn[0]
    sigma = argIn[1]
    
    lognormDistribution = computeLognormDistribution(µ, sigma)
    

    if drawImage == True:

        # compute scipy solution
        lognormScipySolution = computeLognormDistribution(µSciPy, sigmaScipy)
        plt.plot(sizeDistribution, volumeFrequency, color = 'blue', label = 'data')
        plt.plot(sizeDistribution, lognormDistribution, color ='green', label = 'fit')
        plt.plot(sizeDistribution, lognormScipySolution, color ='black', label = 'SciPy')
        plt.legend(loc='upper left')
        plt.xscale('log')
        plt.xlim([xmin,xmax])
        plt.xlabel('size in µm')
        plt.ylabel('size distribution in %')
        plt.title(f'current sigma = {sigma}, current µ = {µ:03f}')
        plt.savefig(os.path.join(currentWorkingDir,f'Distribution-{imageCounter:04d}.png'))
        plt.close()

    deviation = 0
    for i in range(len(volumeFrequency)):
        deviation += abs(volumeFrequency[i] - lognormDistribution[i])
    return deviation

def interfaceToGetDeviation(argIn):
    return getDeviation(argIn, imageCounter=0, drawImage=False)



def isSorted(listA):
    for i in range(len(listA)-1):
        if listA[i] > listA[i+1]:
            return False
    return True

def nelderMead(func, x0):

    # create initial state. We need points u v w 

    def orderByDeviation(func, p1, p2, p3):
        errorOfPs = []
        listOfPs = [p1,p2,p3]
        errorOfP1 = func(p1.values)
        errorOfPs.append(errorOfP1)
        errorOfP2 = func(p2.values)
        errorOfPs.append(errorOfP2)
        errorOfP3 = func(p3.values)
        errorOfPs.append(errorOfP3)
        while not isSorted(errorOfPs):
            for i in range(len(errorOfPs)-1):
                if errorOfPs[i] > errorOfPs[i+1]:
                    placeholderError = errorOfPs[i]
                    errorOfPs[i] = errorOfPs[i+1]
                    errorOfPs[i+1] = placeholderError
                    placeholderP = listOfPs[i]
                    listOfPs[i] = listOfPs[i+1]
                    listOfPs[i+1] = placeholderP


        u = listOfPs[0]
        v = listOfPs[1]
        w = listOfPs[2]
        
        return u, v, w

    
    p1 = vector(x0)
    p2 = vector([x0[0],x0[1]*1.2])
    p3 = vector([x0[0]*1.2,x0[1]])

    u, v, w = orderByDeviation(func, p1,p2,p3)

    vectorUV = u-v

    orthogonalVector = vectorUV.getOrthogonalVector()

    mu = 1./orthogonalVector[1]-(vectorUV[1]/vectorUV[0]*orthogonalVector[0]) * (u[1]-w[1]+(vectorUV[1]/vectorUV[0]*w[0])-(vectorUV[1]/vectorUV[0]*u[0]) )
    p = w+orthogonalVector*mu

    potentialNewP = w + 2*(p-w) 




    

# initial guess
sigma = 0.2
µ = np.log(40)-0.5*sigma**2

# retrieve scipy solution
resultOwnNelderMead = nelderMead(getDeviation, x0 = [µ, sigma])
# resultSciPy = scipy.optimize.minimize(interfaceToGetDeviation, x0 = [µ, sigma],  method='Nelder-Mead')

# µSciPy, sigmaScipy = resultSciPy.x[0], resultSciPy.x[1]
# getDeviation(µ, sigma, imageCounter=0, drawImage=True)









# # Nelder Mead
# u = (x1,y1)
# v = (x2,y2)
# w = (x3,y3)
# simplex = [u, v, w]
# u < v < w
# # dreieck aufbauen zw u, v, w
# vektorUV = u-v
# vektorVW = vector(x3-x2, y3-y2)
# vektorWU = vector(x1-x3, y1-y3)

# #sort
# #reflect
# def reflectWeakestPoint():
#     reflectWOnVectorUV = (vektorUV/2) - w
#     refelectedVector = 2 * (reflectWOnVectorUV - w)
#     reflectedW = refelectedVector + w
#     if reflectedW < w and reflectedW < v and reflectedW > u:
#         w = v
#         v = reflectedW
#     elif reflectedW < w and reflectedW < v and reflectedW < u:
#         if reflectedW *2 < w and reflectedW *2 < v and reflectedW *2 < u:#extend
#             w = v
#             v = u
#             u = reflectedW*2
#         else:
#             w = v
#             v = u
#             u = reflectedW
#     elif reflectedW > w and reflectedW > v and reflectedW > u:
#         shrinkedVector1stHalf = 0.5 *(w - reflectWOnVectorUV)
#         shrinkedVector2ndHalf = 0.5*(refelectedVector -reflectedW)
#         if shrinkedVector1stHalf < w and shrinkedVector1stHalf < v and shrinkedVector1stHalf > u:
#             w = v
#             v = shrinkedVector1stHalf
#         if shrinkedVector2ndHalf < w and shrinkedVector1stHalf < v and shrinkedVector1stHalf > u:
#             w = v
#             v = shrinkedVector2ndHalf
#     else:
#         w = 0.5 * w
#         v = 0.5 * v
#         u = 0.5 * u
# #extend
# #contract
# #shrink
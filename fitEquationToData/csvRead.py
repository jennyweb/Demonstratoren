import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os, shutil

currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, 'sizeDistribution.xlsx')

df = pd.read_excel(dataPath, header=1)
size = []
volume = []
for i in range(len(df['Größe (μm)'])):
    size.append(df['Größe (μm)'][i])
    volume.append(df['% Volumen In'][i])




sigma = 0.2
µ = np.log(40)-0.5*sigma**2
lognormDistribution = []
for i in range(len(size)):
    x = (1./(sigma * size[i] * np.sqrt(2* np.pi))) * np.exp(-((np.log(size[i])-µ)**2)/(2*sigma**2))
    lognormDistribution.append(x)

lognormDistribution = np.array(lognormDistribution)
lognormDistribution *= 100./np.sum(lognormDistribution)

imageCounter = 0
plt.plot(size, volume, color = 'blue', label = 'data')
plt.plot(size, lognormDistribution, color ='green', label = 'lognormDistribution')
plt.legend(loc='upper right')
plt.xscale('log')
plt.xlim([1,1000])
plt.savefig(os.path.join(currentWorkingDir,f'Distribution-{imageCounter:04d}.png'))
plt.close()



class vector:
    def __init__(self,values) -> None:
        self.values = values

    def __len__(self):
        return len(self.values)
        
    def __sub__(self,other):
        if self.len() != other.len():
            return 'unable to perform subtraction'
        new_vector = []
        for i in range(len(self.values)):
            new_vector.append(self.values[i] - other.values[i])
        return new_vector


    def __add__(self,other):
        if self.len() != other.len():
            return 'unable to perform addition'
        new_vector = []
        for i in range(len(self.values)):
            new_vector.append(self.values[i] + other.values[i])
        return new_vector
    
    def __mul__(self, number):
        new_vector = []
        for i in range(len(self.values)):
            new_vector.append(self.values[i] * number)
        return new_vector
    
    def vectorLength(self):
        sumSquare = 0 
        for i in range(len(self.values)):
            sumSquare += (self.values[i])**2
        return np.sqrt(sumSquare)




v = vector([1,3,2])
print(v.vectorLength())

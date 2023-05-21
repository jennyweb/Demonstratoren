import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap

# paths
dir_path = os.path.dirname(os.path.realpath(__file__))

# index assignment
objectIndex = {'stone': 0, 'coal': 1, 'soil': 2, 'hotAir': 3}

# discretization resolution
meshSize = 0.001

totalSize = (0.5, 1.) #in meters
discretization = (np.array(totalSize)/meshSize).astype(int) #number of discretization points
soilSize = (0.05, 1.)
coalSize = (0.1, 1.)
stoneDiameter = 0.2
soilBottomPosition = discretization[0]
soilTopPosition = soilBottomPosition - int(soilSize[0]/meshSize)
coalBottomPosition = soilTopPosition 
coalTopPosition = coalBottomPosition - int(coalSize[0]/meshSize)
stoneCenterOfGravity = (coalTopPosition - int((stoneDiameter/2)/meshSize), int(discretization[1]/2))
objectAssignment = np.ones((discretization[0],discretization[1])) * objectIndex['hotAir'] #assign air as default

for i in range(discretization[0]):
    for j in range(discretization[1]):
        d = ((j - stoneCenterOfGravity[1])**2 + (i - stoneCenterOfGravity[0])**2)**0.5
        if d <=  int((stoneDiameter/2)/meshSize):
            objectAssignment[i,j] = objectIndex['stone']

objectAssignment[coalTopPosition:coalBottomPosition,:] = objectIndex['coal']
objectAssignment[soilTopPosition:soilBottomPosition,:] = objectIndex['soil']

def visualizeObjectAssignement(objectAssignment):
    colors = [(173,156,146), (203,56,23), (100, 78, 20), (249, 178, 75)]
    colorsNormalized = [[x/256. for x in rgbCode] for rgbCode in colors]
    # bins = [-0.5, 0.5, 1.5, 2.5, 3.5]
    cmap = LinearSegmentedColormap.from_list('colorMapObjectAssignment', colorsNormalized, N= 4)
    plt.imshow(objectAssignment, cmap=cmap)
    plt.savefig(f'{dir_path}/objectAssignment.png')

visualizeObjectAssignement(objectAssignment)
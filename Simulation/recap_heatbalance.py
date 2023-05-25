# import numpy as np

# objectIndex = {'stone': 0, 'coal': 1, 'soil':2, 'hot air': 3}

# picSize = (0.5, 1)
# meshSize = 0.001
# descretization = (np.array(picSize)/meshSize).astype(int)

# soilSize = (0.05, 1)
# coalSize = (0.1, 1)
# stoneDiameter = 0.2
# soilBottom = descretization[0]
# soilTop = soilBottom - int(soilSize[0] / meshSize)
# coalBottom = soilTop
# coalTop= coalBottom - int(coalSize[0]/meshSize)
# stoneCenter = coalTop - int((stoneDiameter/2)/meshSize)
# objectAssignment = np.ones((descretization[0], descretization[1])) * objectIndex['hot air']

# for i in range(descretization[0]):
#     for j in range(descretization[1]):
#         d = ((j - stoneCenter[1])**2 + (i - stoneCenter[0])**2)**0.5
#         if d <=  int((stoneDiameter/2)/meshSize):
#             objectAssignment[i,j] = objectIndex['stone']

# objectAssignment[coalBottom : coalTop] = objectIndex['coal']
# objectAssignment[soilBottom : soilTop] = objectIndex['soil']





import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap

# paths
# dir_path = os.path.dirname(os.path.realpath(__file__))

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

objectAssignment[soilTopPosition:soilBottomPosition, :] = objectIndex['soil']
objectAssignment[coalTopPosition:coalBottomPosition, :] = objectIndex['coal']

def visualizeObjectAssignemet(objectAssignment):
    colors = [(173,156,146), (203,56,23), (100,78,20), (249,178,75)]
    colorsNormalized = [[number / 256. for number in color]for color in colors]
    cmap = LinearSegmentedColormap.from_list('colorMapObjectAssignment', colorsNormalized, N= 4)
    plt.imshow(objectAssignment, cmap=cmap)
    plt.savefig('recap_objectAssignment')

visualizeObjectAssignemet(objectAssignment)



isBoundary = np.zeros((discretization[0],discretization[1]))
for i in range(discretization[0]):
    for j in range(discretization[1]):
        if objectAssignment[i,j] == objectIndex['stone']:
            if objectAssignment[i+1][j] !=objectIndex['stone'] or objectAssignment[i-1][j] !=objectIndex['stone'] or objectAssignment[i][j+1] !=objectIndex['stone'] or objectAssignment[i][j-1] !=objectIndex['stone']:
                isBoundary[i][j] = 1

def visualizeIsBoundary(isBoundary):
    colors = [(1,1,1), (0,0,0)]
    cmap = LinearSegmentedColormap.from_list('colorMapIsBoundaryAssignment', colors, N= 3)
    plt.imshow(isBoundary, cmap=cmap)
    plt.savefig('isBoundary.png')

visualizeIsBoundary(isBoundary)

temperatureArray = np.ones((discretization[0],discretization[1])) * 270
temperatureArray[coalTopPosition:coalBottomPosition,:] = 1070
temperatureArray[soilTopPosition:soilBottomPosition,:] = 270
for i in range(discretization[0]):
    for j in range(discretization[1]):
        d = ((j - stoneCenterOfGravity[1])**2 + (i - stoneCenterOfGravity[0])**2)**0.5
        if d <=  int((stoneDiameter/2)/meshSize):
            temperatureArray[i,j] = 390


def visualizeTemperatureField(temperatureArray):
    # cmap = LinearSegmentedColormap.from_list('colorMaptempArray', N= 4)
    plt.imshow(objectAssignment, cmap='hot')
    plt.savefig('recap_temperatureArrayt')

visualizeTemperatureField(temperatureArray)

t = 0
tmax = 100
dT = 0.001
iteration = 0
for i in range(tmax):
    t = t + dT
    iteration += 1
    if iteration % 100 == 0:
        visualizeTemperatureField(temperatureArray)
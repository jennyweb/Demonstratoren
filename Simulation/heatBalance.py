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
    colors = [(173,156,146), (203,56,23), (100,78,20), (249,178,75)]
    colorsNormalized = [[x/256. for x in rgbCode] for rgbCode in colors]
    # bins = [-0.5, 0.5, 1.5, 2.5, 3.5]
    cmap = LinearSegmentedColormap.from_list('colorMapObjectAssignment', colorsNormalized, N= 4)
    plt.imshow(objectAssignment, cmap=cmap)
    plt.savefig(f'{dir_path}/objectAssignment.png')
    plt.close

visualizeObjectAssignement(objectAssignment)


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
    plt.savefig(f'{dir_path}/isBoundary.png')
    plt.close

visualizeIsBoundary(isBoundary)

temperatureArray = np.ones((discretization[0],discretization[1])) * 270
temperatureArray[coalTopPosition:coalBottomPosition,:] = 1070
temperatureArray[soilTopPosition:soilBottomPosition,:] = 270
for i in range(discretization[0]):
    for j in range(discretization[1]):
        d = ((j - stoneCenterOfGravity[1])**2 + (i - stoneCenterOfGravity[0])**2)**0.5
        if d <=  int((stoneDiameter/2)/meshSize):
            temperatureArray[i,j] = 390


def visualizeTemperatureField(temperatureArray, filename):
    # cmap = LinearSegmentedColormap.from_list('colorMaptempArray', N= 4)
    plt.imshow(temperatureArray, cmap='hot')
    plt.savefig(f'{dir_path}/TemperatureArray{filename}t')
    plt.close()


cpDict = {objectIndex['stone']: 1, objectIndex['coal']: 1.02, objectIndex['soil']: 0.8, objectIndex['hotAir']: 1.005} #in kJ kg-1 K-1  ; urch Erhöhung der Pyrolyseendtemperatur von 400 auf 1200 °C steigt die spezifische Wärme der H. von 1,02 auf 1,60 kJ/kg K an
densityDict = {objectIndex['stone']: 2.5, objectIndex['coal']: 0.25, objectIndex['soil']: 0.92, objectIndex['hotAir']: 0.783 } # in g cm-3 
thermalConductivityDict = {objectIndex['stone']: 2.0, objectIndex['hotAir']: 0.02} #in J s-1 m-1 K-1

def getcp(i,j):
    oa = objectAssignment[i,j]
    cp = cpDict[oa]
    return cp

def getDensity(i,j):
    oa = objectAssignment[i,j]
    density = densityDict[oa]
    return density

def getMass(i,j):
    volumen = meshSize**2
    mass = getDensity(i,j) * volumen
    return mass

enthalpyArray = np.ones((discretization[0],discretization[1])) 
for i in range(discretization[0]):
    for j in range(discretization[1]):
        if objectAssignment[i,j] == objectIndex['stone']:
            enthalpyArray[i,j] == getMass(i,j) * getcp(i,j) * temperatureArray[i,j]

for i in range(discretization[0]):
    for j in range(discretization[1]):
        if objectAssignment[i,j] == objectIndex['coal']:
            enthalpyArray[i,j] == getMass(i,j) * getcp(i,j) * temperatureArray[i,j]

for i in range(discretization[0]):
    for j in range(discretization[1]):
        if objectAssignment[i,j] == objectIndex['soil']:
            enthalpyArray[i,j] == getMass(i,j) * getcp(i,j) * temperatureArray[i,j]

for i in range(discretization[0]):
    for j in range(discretization[1]):
        if objectAssignment[i,j] == objectIndex['hotAir']:
            enthalpyArray[i,j] == getMass(i,j) * getcp(i,j) * temperatureArray[i,j]

def visualizeEnthalpyArray(enthalpyArray,filename):
    plt.imshow(enthalpyArray, cmap='hot')
    plt.savefig(f'{dir_path}/{filename}')
    plt.close

visualizeEnthalpyArray(enthalpyArray,1)

t = 0
tmax = 100
dT = 0.001
iteration = 0
picNumber = 1
while t < tmax:
    t = t + dT
    iteration += 1
    if iteration % 100 == 0:
        picNumber += 1
        filename = (f'{picNumber}')
        # visualizeTemperatureField(temperatureArray, filename)
        # visualizeEnthalpyArray(enthalpyArray, filename)





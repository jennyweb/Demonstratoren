import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

# paths
dir_path = os.path.dirname(os.path.realpath(__file__))

# index assignment
objectIndex = {'stone': 0, 'coal': 1, 'soil': 2, 'hotAir': 3}

# discretization resolution
meshSize = 0.005

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

# array asignment
objectAssignment = np.ones((discretization[0],discretization[1])) * objectIndex['hotAir'] #assign air as default

for i in range(discretization[0]):
    for j in range(discretization[1]):
        d = ((j - stoneCenterOfGravity[1])**2 + (i - stoneCenterOfGravity[0])**2)**0.5
        if d <=  int((stoneDiameter/2)/meshSize):
            objectAssignment[i,j] = objectIndex['stone']

objectAssignment[coalTopPosition:coalBottomPosition,:] = objectIndex['coal']
objectAssignment[soilTopPosition:soilBottomPosition,:] = objectIndex['soil']

isBoundary = np.zeros((discretization[0],discretization[1]))
for i in range(discretization[0]):
    for j in range(discretization[1]):
        if objectAssignment[i,j] == objectIndex['stone']:
            if objectAssignment[i+1][j] !=objectIndex['stone'] or objectAssignment[i-1][j] !=objectIndex['stone'] or objectAssignment[i][j+1] !=objectIndex['stone'] or objectAssignment[i][j-1] !=objectIndex['stone']:
                isBoundary[i][j] = 1

temperatureArray = np.ones((discretization[0],discretization[1])) * 270
temperatureArray[coalTopPosition:coalBottomPosition,:] = 1070
temperatureArray[soilTopPosition:soilBottomPosition,:] = 270
for i in range(discretization[0]):
    for j in range(discretization[1]):
        d = ((j - stoneCenterOfGravity[1])**2 + (i - stoneCenterOfGravity[0])**2)**0.5
        if d <=  int((stoneDiameter/2)/meshSize):
            temperatureArray[i,j] = 390

#physical constants and used variables
sigma = 5.67037321 * 10**-8 # Boltzmann constant W m-2 K-4
epsilon = 0.3 # emissivity factor
A = meshSize #m
Ta = 278 # ambient surrounding temperature K
Tair = 278 # surrounding air temperature K

t = 0
tmax = 100
dt = 0.1
iteration = 0
picNumber = 1

cpDict = {objectIndex['stone']: 1, objectIndex['coal']: 1.02, objectIndex['soil']: 0.8, objectIndex['hotAir']: 1.005} #in kJ kg-1 K-1  ; urch Erhöhung der Pyrolyseendtemperatur von 400 auf 1200 °C steigt die spezifische Wärme der H. von 1,02 auf 1,60 kJ/kg K an
densityDict = {objectIndex['stone']: 2.5e3, objectIndex['coal']: 0.25e3, objectIndex['soil']: 0.92e3, objectIndex['hotAir']: 0.783e3 } # in g cm-3 
thermalConductivityDict = {objectIndex['stone']: 2.0, objectIndex['hotAir']: 0.02} #in J s-1 m-1 K-1


def visualizeObjectAssignement(objectAssignment):
    colors = [(173,156,146), (203,56,23), (100,78,20), (249,178,75)]
    colorsNormalized = [[x/256. for x in rgbCode] for rgbCode in colors]
    # bins = [-0.5, 0.5, 1.5, 2.5, 3.5]
    cmap = LinearSegmentedColormap.from_list('colorMapObjectAssignment', colorsNormalized, N= 4)
    plt.imshow(objectAssignment, cmap=cmap)
    plt.savefig(f'{dir_path}/Images/objectAssignment.png')
    plt.close()

visualizeObjectAssignement(objectAssignment)

def visualizeIsBoundary(isBoundary):
    colors = [(1,1,1), (0,0,0)]
    cmap = LinearSegmentedColormap.from_list('colorMapIsBoundaryAssignment', colors, N= 3)
    plt.imshow(isBoundary, cmap=cmap)
    plt.savefig(f'{dir_path}/Images/isBoundary.png')
    plt.close()

visualizeIsBoundary(isBoundary)

def visualizeTemperatureField(temperatureArray, filename):
    # cmap = LinearSegmentedColormap.from_list('colorMaptempArray', N= 4)
    plt.imshow(temperatureArray, cmap='hot')
    plt.savefig(f'{dir_path}/Images/{filename}')
    plt.close()

getcp = lambda i,j: cpDict[objectAssignment[i,j]]
# def getcp(i,j):
#     oa = objectAssignment[i,j]
#     cp = cpDict[oa]
#     return cp
getDensity = lambda i,j: densityDict[objectAssignment[i,j]]
# def getDensity(i,j):
#     oa = objectAssignment[i,j]
#     density = densityDict[oa]
#     return density
getMass = lambda i,j: getDensity(i,j) * meshSize**2
# def getMass(i,j):
#     volumen = meshSize**2
#     mass = getDensity(i,j) * volumen
#     return mass

def getEnthalpyArray(temperatureArray):
    enthalpyArray = np.ones((discretization[0],discretization[1])) 
    for i in range(discretization[0]):
        for j in range(discretization[1]):
                enthalpyArray[i,j] = getMass(i,j) * getcp(i,j) * temperatureArray[i,j]
    return enthalpyArray

def visualizeEnthalpyArray(enthalpyArray,filename):
    ax = plt.subplot()
    im = ax.imshow(np.arange(100).reshape((10,10)))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size = "5%", pad = 0.05)
    plt.colorbar(im,cax= cax)
    plt.imshow(enthalpyArray, cmap='hot')
    plt.savefig(f'{dir_path}/Images/{filename}')
    plt.close()

def getTempArrayFromEnthalpie(enthalpyArray):
    temperatureArray = np.ones((discretization[0],discretization[1])) 
    for i in range(discretization[0]):
        for j in range(discretization[1]):
            temperatureArray[i,j] = enthalpyArray[i,j] / (getcp(i,j) * getMass(i,j))
    return temperatureArray

enthalpyArray = getEnthalpyArray(temperatureArray)
#begin simulation
while t < tmax:
    #increase counter
    t = t + dt
    temperatureArray = getTempArrayFromEnthalpie(enthalpyArray)
    # apply physics
    enthalpyRateArray = np.zeros((discretization[0], discretization[1]))
    for i in range(discretization[0]):
        for j in range(discretization[1]):
            if isBoundary[i,j] == 1:
                enthalpyRateArray[i,j] = -epsilon * sigma * A * ((temperatureArray[i,j])**4 - Ta**4)
    enthalpyArray = enthalpyArray + enthalpyRateArray * dt
    #visual output
    iteration += 1
    if iteration % 100 == 0:
        picNumber += 1
        filenameTemperature = (f'temperature-{picNumber:02d}.png')
        filenameEnthalpy = (f'enthalpy-{picNumber:02d}.png')
        visualizeTemperatureField(temperatureArray, filenameTemperature)
        visualizeEnthalpyArray(enthalpyArray, filenameEnthalpy)









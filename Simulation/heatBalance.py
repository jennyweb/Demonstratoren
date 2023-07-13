import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from alive_progress import alive_bar
import shutil

# paths
dir_path = os.path.dirname(os.path.realpath(__file__))

# create intermediate folders
if os.path.isdir(f'{dir_path}/Images'):
    shutil.rmtree(f'{dir_path}/Images')
os.mkdir(f'{dir_path}/Images')

# index assignment
objectIndex = {'stone': 0, 'coal': 1, 'soil': 2, 'hotAir': 3}

# discretization resolution
meshSize = 0.001

totalSize = (0.5, 1.) #in meters
discretization = (np.array(totalSize)/meshSize).astype(int) #number of discretization points
soilSize = (0.05, 1.)
coalSize = (0.1, 0.75)
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

objectAssignment[coalTopPosition:soilBottomPosition,:] = objectIndex['hotAir']
edges = int((totalSize[1] - coalSize[1]) / meshSize / 2)
objectAssignment[coalTopPosition:coalBottomPosition,edges:int(totalSize[1] / meshSize)-edges] = objectIndex['coal']

isBoundary = np.zeros((discretization[0],discretization[1]))
isBoundaryToCoal = np.zeros((discretization[0],discretization[1]))
isBoundaryToAir = np.zeros((discretization[0],discretization[1]))
isWithinStone = np.zeros((discretization[0], discretization[1]))
isWithinCoal = np.zeros((discretization[0], discretization[1]))
for i in range(discretization[0]):
    for j in range(discretization[1]):
        if objectAssignment[i,j] == objectIndex['stone']:
            if objectAssignment[i+1][j] !=objectIndex['stone'] or objectAssignment[i-1][j] !=objectIndex['stone'] or objectAssignment[i][j+1] !=objectIndex['stone'] or objectAssignment[i][j-1] !=objectIndex['stone']:
                isBoundary[i][j] = 1
            if objectAssignment[i+1][j] == objectIndex['stone'] and objectAssignment[i-1][j] ==objectIndex['stone'] and objectAssignment[i][j+1] ==objectIndex['stone'] and objectAssignment[i][j-1] ==objectIndex['stone']:
                isWithinStone[i][j] = 1
        if objectAssignment[i,j] == objectIndex['coal']:
            if objectAssignment[min(i+1,discretization[0]-1)][j] == objectIndex['coal'] and objectAssignment[max(i-1,0)][j] ==objectIndex['coal'] and objectAssignment[i][min(j+1,discretization[1]-1)] ==objectIndex['coal'] and objectAssignment[i][max(j-1, 0)] ==objectIndex['coal']:
                isWithinCoal[i][j] = 1
        if isBoundary[i,j] == 1:
            if objectAssignment[i+1][j] == objectIndex['coal'] or objectAssignment[i-1][j] == objectIndex['coal'] or objectAssignment[i][j+1] == objectIndex['coal'] or objectAssignment[i][j-1] == objectIndex['coal']:
                isBoundaryToCoal[i][j] = 1
            if objectAssignment[i+1][j] == objectIndex['hotAir'] or objectAssignment[i-1][j] == objectIndex['hotAir'] or objectAssignment[i][j+1] == objectIndex['hotAir'] or objectAssignment[i][j-1] == objectIndex['hotAir']:
                isBoundaryToAir[i][j] = 1



IndexToHeight = lambda i : totalSize[0]-totalSize[0]/discretization[0]*i
heightToTemperature = lambda h : 800/(totalSize[0]-(soilSize[0]+coalSize[0]))*(h-(soilSize[0]+coalSize[0]))+600

Tair = np.ones((discretization[0],discretization[1])) * 270
for i in range(discretization[0]):
    Tair[i,edges:int(totalSize[1] / meshSize)-edges] = heightToTemperature(IndexToHeight(i))


temperatureArray = np.ones((discretization[0],discretization[1])) * 270
temperatureArray[coalTopPosition:coalBottomPosition,edges:int(totalSize[1] / meshSize)-edges] = 1070
# temperatureArray[soilTopPosition:soilBottomPosition,:] = 270
# for i in range(discretization[0]):
#     for j in range(discretization[1]):
#         d = ((j - stoneCenterOfGravity[1])**2 + (i - stoneCenterOfGravity[0])**2)**0.5
#         if d <=  int((stoneDiameter/2)/meshSize):
#             temperatureArray[i,j] = 390

#physical constants and used variables
sigma = 5.67037321 * 10**-8 # Boltzmann constant W m-2 K-4
epsilon = 0.3 # emissivity factor without unit
A = meshSize**2 #m
Ta = 278 # ambient surrounding temperature K

t = 0
tend = 1
dt = 0.1
iteration = 0
picNumber = 0
numberOfIterations = tend/dt

cpDict = {objectIndex['stone']: 1, objectIndex['coal']: 1.02, objectIndex['soil']: 0.8, objectIndex['hotAir']: 1.005} #in kJ kg-1 K-1 
densityDict = {objectIndex['stone']: 2.5e3, objectIndex['coal']: 0.25e3, objectIndex['soil']: 0.92e3, objectIndex['hotAir']: 0.783 } # in kg cm-3 
thermalConductivityDict = {objectIndex['stone']: 2.0, objectIndex['hotAir']: 0.02} #in J s-1 m-1 K-1


def visualizeObjectAssignment(objectAssignment):
    colors = [(173,156,146), (203,56,23), (100,78,20), (249,178,75)]
    colorsNormalized = [[x/256. for x in rgbCode] for rgbCode in colors]
    cmap = LinearSegmentedColormap.from_list('colorMapObjectAssignment', colorsNormalized, N= 4)
    plt.imshow(objectAssignment, cmap=cmap)
    plt.savefig(f'{dir_path}/Images/objectAssignment.png')
    plt.close()

def visualizeArray(objectAssignment, testArray, filename):
    colors = [(173,156,146), (203,56,23), (100,78,20), (249,178,75)]
    colorsNormalized = [[x/256. for x in rgbCode] for rgbCode in colors]
    blackAndWhiteRGB = [(1,1,1), (0,0,0)]
    cmap = LinearSegmentedColormap.from_list('colorMapObjectAssignment', colorsNormalized, N= 4)
    cmapBW = LinearSegmentedColormap.from_list('colorMapIsBoundaryAssignment', blackAndWhiteRGB, N= 3)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3))
    plt.axis('off')
    axs[0].imshow(objectAssignment, cmap=cmap)
    axs[1].imshow(testArray, cmap=cmapBW)
    fig.suptitle(filename[:-4])
    plt.savefig(f'{dir_path}/Images/{filename}')
    plt.close()


def visualizeTemperatureField(filename, time, temperatureArray):
    temperatureOutput = np.zeros((discretization[0], discretization[1]))
    for i in range(discretization[0]):
        for j in range(discretization[1]):
            if objectAssignment[i,j] == objectIndex['hotAir']:
                temperatureOutput[i,j] = Tair[i,j]
            elif objectAssignment[i,j] == objectIndex['soil'] or objectAssignment[i,j] == objectIndex['coal'] or objectAssignment[i,j] == objectIndex['stone']:
                temperatureOutput[i,j] = temperatureArray[i,j]
            else:
                raise RuntimeError('Jenny, you need to implement this!')

    ax = plt.subplot()
    plt.axis('off')
    colors = [(12,4,5), (229,37,32), (240,125,25), (246,235,97)]
    colorsNormalized = [[x/256. for x in rgbCode] for rgbCode in colors]
    cmap = LinearSegmentedColormap.from_list('colorMapObjectAssignment', colorsNormalized)
    im = plt.imshow(temperatureOutput-273, cmap=cmap, vmin=0) # temperature in degree Celsius
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size = "5%", pad = 0.05)
    cbar = plt.colorbar(im,cax= cax)
    cbar.set_label('$T$ in degree C', rotation = 270)
    plt.title(f't = {time/60:1.2f} min')
    plt.savefig(f'{dir_path}/Images/{filename}')
    plt.close()

getcp = lambda i,j: cpDict[objectAssignment[i,j]]
getDensity = lambda i,j: densityDict[objectAssignment[i,j]]
getMass = lambda i,j: getDensity(i,j) * meshSize**2

def getHeatTransferCoefficient(interface):
    """
    the heat transfer coefficient depends on whether the stone has contact to air or coal.
    Input:
        interface : int
        interface either objectIndex['hotAir'] or objectIndex['coal']
    Usage:
        getHeatTransferCoefficient(objectIndex['hotAir'])
    """
    if interface == objectIndex['hotAir']:
        return 25.
    elif interface == objectIndex['coal']:
        return 1000.
     
def getHeatConductivity(object):
    """
    this function returns the heat conductivity in W / (m K) for a given object

    Input:
        object: int
        object either objectIndex['soil'] or objectIndex['coal'] or objectIndex['stone']
    Usage:
        getHeatConductivity(objectIndex['soil'])
    """
    heatConductivity = {objectIndex['coal']: 0.3, objectIndex['soil']: 1, objectIndex['stone']: 10}
    if object not in heatConductivity.keys():
        raise RuntimeError(f'heat conductivity for object {object} is not available')
    return heatConductivity[object]
    

def getEnthalpyArray(temperatureArray):
    enthalpyArray = np.ones((discretization[0],discretization[1])) 
    for i in range(discretization[0]):
        for j in range(discretization[1]):
                enthalpyArray[i,j] = getMass(i,j) * getcp(i,j) * temperatureArray[i,j]
    return enthalpyArray

def visualizeEnthalpyField(enthalpyArray,filename):
    ax = plt.subplot()
    plt.axis('off')
    im = plt.imshow(enthalpyArray, cmap='hot')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size = "5%", pad = 0.05)
    cbar = plt.colorbar(im,cax= cax)
    cbar.set_label('$H$ in J')
    plt.savefig(f'{dir_path}/Images/{filename}')
    plt.close()

def getTempArrayFromEnthalpie(enthalpyArray):
    temperatureArray = np.ones((discretization[0],discretization[1])) 
    for i in range(discretization[0]):
        for j in range(discretization[1]):
            temperatureArray[i,j] = enthalpyArray[i,j] / (getcp(i,j) * getMass(i,j))
    return temperatureArray

def applyHeatConduction(i,j):
    for object in ['stone', 'soil', 'coal']:
        if objectAssignment[i,j] == objectIndex[object]:
            if i+1 < discretization[0]:
                if objectAssignment[i+1,j] == objectIndex[object]:
                    conductionEnthalpy = A * getHeatConductivity(objectIndex[object]) * (temperatureArray[i,j]- temperatureArray[i+1,j]) / meshSize
                    enthalpyRateArray[i,j] -= conductionEnthalpy
                    enthalpyRateArray[i+1,j] += conductionEnthalpy

            if i-1 > 0:
                if objectAssignment[i-1,j] == objectIndex[object]:
                    conductionEnthalpy = A * getHeatConductivity(objectIndex[object]) * (temperatureArray[i,j]- temperatureArray[i-1,j]) / meshSize
                    enthalpyRateArray[i,j] -= conductionEnthalpy
                    enthalpyRateArray[i-1,j] += conductionEnthalpy

            if j+1 < discretization[1]:
                if objectAssignment[i,j+1] == objectIndex[object]:
                    conductionEnthalpy = A * getHeatConductivity(objectIndex[object]) * (temperatureArray[i,j]- temperatureArray[i,j+1]) / meshSize
                    enthalpyRateArray[i,j] -= conductionEnthalpy
                    enthalpyRateArray[i,j+1] += conductionEnthalpy

            if j-1 > 0:
                if objectAssignment[i,j-1] == objectIndex[object]:
                    conductionEnthalpy = A * getHeatConductivity(objectIndex[object]) * (temperatureArray[i,j]- temperatureArray[i,j-1]) / meshSize
                    enthalpyRateArray[i,j] -= conductionEnthalpy
                    enthalpyRateArray[i,j-1] += conductionEnthalpy


visualizeObjectAssignment(objectAssignment)
visualizeArray(objectAssignment, isBoundary, 'isBoundary.png')
visualizeArray(objectAssignment, isBoundaryToAir, 'isBoundaryToAir.png')
visualizeArray(objectAssignment, isBoundaryToCoal, 'isBoundaryToCoal.png')
visualizeArray(objectAssignment, isWithinCoal, 'isWithinCoal.png')
visualizeArray(objectAssignment, isWithinStone, 'isWithinStone.png')
enthalpyArray = getEnthalpyArray(temperatureArray)

#begin simulation
with alive_bar(int(numberOfIterations)+1) as bar:
    while t < tend:

        # recover temperature array from enthalpy
        temperatureArray = getTempArrayFromEnthalpie(enthalpyArray)

        # apply physics
        enthalpyRateArray = np.zeros((discretization[0], discretization[1]))
        for i in range(discretization[0]):
            for j in range(discretization[1]):
                # boundary related physics
                if isBoundaryToAir[i,j] == 1:

                    # radiation
                    enthalpyRateArray[i,j] -= epsilon * sigma * A * ((temperatureArray[i,j])**4 - Ta**4)

                    # convection
                    enthalpyRateArray[i,j] -= getHeatTransferCoefficient(objectIndex['hotAir']) * A * (temperatureArray[i,j]-Tair[i,j])

                if isBoundaryToCoal[i,j] == 1:
                    # convection
                    convectionEnthalpy = getHeatTransferCoefficient(objectIndex['coal']) * A * (temperatureArray[i,j]-temperatureArray[i+1,j])
                    enthalpyRateArray[i,j] -= convectionEnthalpy
                    enthalpyRateArray[i+1,j] += convectionEnthalpy
           
                applyHeatConduction(i,j)

        enthalpyArray = enthalpyArray + enthalpyRateArray * dt

        #visual output
        if iteration % 30 == 0:
            filenameTemperature = (f'temperature-{picNumber:04d}.png')
            filenameEnthalpy = (f'enthalpy-{picNumber:04d}.png')
            visualizeTemperatureField(filenameTemperature, t, temperatureArray)
            visualizeEnthalpyField(enthalpyArray, filenameEnthalpy)
            picNumber += 1
        
        #increase counter
        t = t + dt
        bar()
        iteration += 1




print('Note: The simulation time has been shortened for demonstration purpose. Re-run the script again with tend = 1000 in line 94')




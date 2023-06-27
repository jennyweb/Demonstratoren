import pandas as pd
import os
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, 'diveTableMeters.xlsx')

# creating random dive profile

depth = [0]
time = [0]
np.random.seed(497)
depthNp = np.random.randint(-42,-10, 1).tolist()
timeNp = np.random.randint(5,40, 1).tolist()
surfaceTime = np.random.randint(10,70,1).tolist()
maxDepthSecondDive = depthNp[0]
depthSecondDive = np.random.randint(maxDepthSecondDive,-10, 1).tolist()
for i in range(2):
    depth.append(depthNp[0])
for i in range(2):
    depth.append(0)
for i in range(2):
    depth.append(depthSecondDive[0])
depth.append(0)
for i in range(len(timeNp)):
    time.append(time[-1]+1)
    time.append(timeNp[0]+time[-1])
time.append(time[-1]+1)
time.append(time[-1] +surfaceTime[0])
time.append(time[-1]+1)

dataForDiveComputerDepthTime = []
for i in range(2,len(time)):
    if i % 2 == 0:
        dataForDiveComputerDepthTime.append((depth[i],(time[i]-time[i-1])))




# visualization of dive profile and pressure groups
def visualizeDivingProfile(time,depth,filename):    
    plt.plot(time,depth)
    plt.title(filename)
    plt.xlabel('time in s')
    plt.ylabel('depth in m')
    plt.savefig(os.path.join(currentWorkingDir, f'{filename}.png'))
    plt.close()

# saving depth and time to .txt file
def writeDataForDivingComputer(dataForDiveComputerDepthTime,filename):
    with open(os.path.join(currentWorkingDir, f'{filename}.txt'),'w') as fout:
        fout.write('depth time\n')
        for i in range(len(dataForDiveComputerDepthTime)):
            fout.write(f'{dataForDiveComputerDepthTime[i]}\n')
    

# reading in data from table 1: Pressure group after first dive
findPressureGroup = {}
dfFindPressureGroup = pd.read_excel(dataPath, sheet_name='find pressure group (meter)')
keysInFindPressureGroup = []
for i,column_name in enumerate(dfFindPressureGroup):
    if i > 0:
        key = float(f'{float(column_name):1.02f}')
        keysInFindPressureGroup.append(key)
        findPressureGroup[key] = dfFindPressureGroup[column_name]
    else:
        pressureGroup = dfFindPressureGroup[column_name]
keysInFindPressureGroup.sort(reverse=True)

depthAndTime = dataForDiveComputerDepthTime
desiredDepth2ndDive = depthSecondDive

def getKeyForDepth(depth):
    if depth > keysInFindPressureGroup[0]:
        raise RuntimeError (f'please make sure that the depth does not exceed 42m. I got {depth}')
        
    for i in range(len(keysInFindPressureGroup)):
        if abs(depth) >= keysInFindPressureGroup[i]:
            key = keysInFindPressureGroup[i-1]
            return key
    return keysInFindPressureGroup[-1]
    

key = getKeyForDepth(depthAndTime[0][0])

def getPressureGroup(key,time):
    pressureGroupforTt = None
    minutesInCertainDepth = findPressureGroup[key]
    for i in range(len(minutesInCertainDepth)):
        if minutesInCertainDepth[i] >= time:
            pressureGroupforTt = pressureGroup[i]
            return pressureGroupforTt
   
print(getPressureGroup(key,depthAndTime[0][1]))

# reading in data from table 2: Pressure group after surface intervall
pressureGroupAfterSurfaceIntervall = pd.read_excel(dataPath, sheet_name='get new pressure group')
mappingSurfaceTimeToNewPgroup = {} 
listmappingSurfaceTimeToNewPgroup = []
indexToPressureGroup = {}
for i,oldPGroup in enumerate(pressureGroupAfterSurfaceIntervall[ 'pressure group from table 1 new pressure group']):
    if not pd.isnull(oldPGroup):
        listmappingSurfaceTimeToNewPgroup.append(oldPGroup)
        indexToPressureGroup[i] = oldPGroup
        indexToPressureGroup[i+1] = oldPGroup
        mappingSurfaceTimeToNewPgroup[oldPGroup] = {}

for i,column_name in enumerate(pressureGroupAfterSurfaceIntervall):
    if i == 0: #skip first row
        continue
    for j in range(len(pressureGroupAfterSurfaceIntervall)):
        if j % 2 != 0: #skips everysecond row because of time intervall
            continue
        if not pd.isnull(pressureGroupAfterSurfaceIntervall[column_name].iloc[j]):
            mappingSurfaceTimeToNewPgroup[indexToPressureGroup[j]][pressureGroupAfterSurfaceIntervall[column_name].iloc[j]] = column_name

oldPG = getPressureGroup(key,depthAndTime[0][1])

if depthAndTime[1][1] > 59:
    hour, minutes= divmod(depthAndTime[1][1], 60)
else:
    hour = 0
    minutes = depthAndTime[1][1]

surfaceTime = datetime.time(hour,minutes)

def getPressureGrAfterSurfaceIntervall(oldPG, surfaceTime):
    adequateTimeIntervall = 0
    timezones = list(mappingSurfaceTimeToNewPgroup[oldPG].keys())
    timezones.sort()
    for i in range(len(timezones)):
        if surfaceTime < timezones[i]:
            adequateTimeIntervall = timezones[i-1]
            break
    return mappingSurfaceTimeToNewPgroup[oldPG][adequateTimeIntervall]

print(getPressureGrAfterSurfaceIntervall(oldPG, surfaceTime))

# reading in data from table 3: Maximum bottom time at desired depth
dfBottomTimeSecondDive = pd.read_excel(dataPath, sheet_name='max bottom time 2nd dive')
residualNitrogenTime = {}
maxBottomTime = {}
oldPGInBottomTime = []
depthsfor2ndDive = []
indexBottomTime = {}
indexResNitrogen = {}
for i,column_name in enumerate(dfBottomTimeSecondDive):
    if i > 0:
        keyPG = column_name
        oldPGInBottomTime.append(keyPG)
        maxBottomTime[column_name] = {}
        residualNitrogenTime[column_name] = {}
for i,depth2ndDive in enumerate(dfBottomTimeSecondDive['depth in m pressure group at the end of surface intervall']):
    if not pd.isnull(depth2ndDive):
        depth2ndDive = float(f'{float(depth2ndDive):1.02f}')
        depthsfor2ndDive.append(depth2ndDive)
        indexBottomTime[i+1] =depth2ndDive
        indexResNitrogen[i] = depth2ndDive
depthsfor2ndDive.sort()
for i, column_name in enumerate(dfBottomTimeSecondDive):
    if i == 0:
        continue
    counter = 1
    counterN2 = 0
    for j in range(len(depthsfor2ndDive)):
            
            if not pd.isnull(dfBottomTimeSecondDive[column_name].iloc[j]):
                maxBottomTime[column_name][depthsfor2ndDive[j]] = dfBottomTimeSecondDive[column_name].iloc[counter]
            counter += 2
            if not pd.isnull(dfBottomTimeSecondDive[column_name].iloc[j]):
                residualNitrogenTime[column_name][depthsfor2ndDive[j]] = dfBottomTimeSecondDive[column_name].iloc[counterN2]
            counterN2 += 2

def getMaxBottomTime(currenPG, desiredDivingDepth):
    desiredDivingDepthGroup = None
    maximumBottomTime = 0
    for i in range(len(depthsfor2ndDive)):
        if abs(desiredDivingDepth[0]) < depthsfor2ndDive[i]:
            desiredDivingDepthGroup = depthsfor2ndDive[i]
            print(desiredDivingDepthGroup)
            break
    maximumBottomTime = maxBottomTime[currenPG][desiredDivingDepthGroup]
    time.append(int(time[-1]+maximumBottomTime))
    time.append(time[-1]+1)
    return maximumBottomTime, time

maximumBottomTime, time = getMaxBottomTime(getPressureGrAfterSurfaceIntervall(oldPG, surfaceTime), desiredDepth2ndDive)
filename = f'divingprofile_{depthAndTime[0][0]}'
visualizeDivingProfile(time,depth, filename)
writeDataForDivingComputer(depthAndTime, filename)





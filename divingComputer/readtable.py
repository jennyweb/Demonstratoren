import pandas as pd
import os
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(497)


def getKeyForDepth(depth):
    if depth > keysInFindPressureGroup[0]:
        raise RuntimeError (f'please make sure that the depth does not exceed 42m. I got {depth}')
        
    for i in range(len(keysInFindPressureGroup)):
        if abs(depth) >= keysInFindPressureGroup[i]:
            key = keysInFindPressureGroup[i-1]
            return key
    return keysInFindPressureGroup[-1]

def getPressureGroup(key,time):
    pressureGroupforTt = None
    minutesInCertainDepth = findPressureGroup[key]
    for i in range(len(minutesInCertainDepth)):
        if minutesInCertainDepth[i] >= time:
            pressureGroupforTt = pressureGroup[i]
            return pressureGroupforTt
        
def getmaxTime1stDive(key):
    maxTimeDive1 = 0
    for i in range(len(findPressureGroup[key])):
        if  np.isnan(findPressureGroup[key][i]):
            maxTimeDive1 = findPressureGroup[key][i-1]
        return maxTimeDive1
        


# visualization of dive profile and pressure groups
def visualizeDivingProfile(time,depth,filename):    
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(time, depth, color = 'green',lw=2)
    plt.title(filename)
    plt.xlabel('time in min')
    plt.ylabel('depth in m')
    ax.annotate(f'PG1 = {oldPG}', xy=(time[2], 0.25), color= 'blue')
    ax.annotate(f'PG2 = {currentPG}', xy=(time[4]-3,0.25), color= 'blue')
    ax.annotate(f'PG3 = {PG3}', xy=(time[6]-3,0.25), color= 'blue')
    ax.annotate(f'BT = {depthAndTime[0][1]} min', xy=(time[1]+1,depth[1]+0.25), color= 'orange')
    ax.annotate(f'ST = {depthAndTime[1][1]} min', xy=(time[4]/2,depth[3]+0.25), color= 'orange')
    ax.annotate(f'BT = {int(maximumBottomTime)} min', xy=(time[5]+1,depth[5]+0.25), color= 'orange')
    plt.savefig(os.path.join(currentWorkingDir, f'{filename}.png'))
    plt.close()


# saving depth and time to .txt file
def writeDataForDivingComputer(dataForDiveComputerDepthTime,filename):
    with open(os.path.join(currentWorkingDir, f'{filename}.txt'),'w') as fout:
        fout.write('depth time\n')
        for i in range(len(dataForDiveComputerDepthTime)):
            fout.write(f'{dataForDiveComputerDepthTime[i]}\n')


def getPressureGrAfterSurfaceIntervall(oldPG, surfaceTime):
    adequateTimeIntervall = 0
    timezones = list(mappingSurfaceTimeToNewPgroup[oldPG].keys())
    timezones.sort()
    for i in range(len(timezones)):
        if surfaceTime < timezones[i]:
            adequateTimeIntervall = timezones[i-1]
            break
    return mappingSurfaceTimeToNewPgroup[oldPG][adequateTimeIntervall]


def getMaxBottomTime(currenPG, desiredDivingDepth):
    desiredDivingDepthGroup = None
    maximumBottomTime = 0
    for i in range(len(depthsfor2ndDive)):
        if abs(desiredDivingDepth[0]) < depthsfor2ndDive[i]:
            desiredDivingDepthGroup = depthsfor2ndDive[i]
            break
    maximumBottomTime = maxBottomTime[currenPG][desiredDivingDepthGroup]
    resN2Time = residualNitrogenTime[currenPG][desiredDivingDepthGroup]
    time.append(int(time[-1]+maximumBottomTime))
    time.append(time[-1]+1)
    return maximumBottomTime, time, resN2Time

def getPressureGroupAfter2ndDive(maximumBottomTime, resN2Time):
    totalBottomTime = maximumBottomTime + resN2Time
    key2ndDive = getKeyForDepth(desiredDepth2ndDive[0])
    PG3 = getPressureGroup(key2ndDive,totalBottomTime)
    return PG3



########################################################################
# open Excel sheet
########################################################################

currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, 'diveTableMeters.xlsx')




########################################################################
# reading in data from table 1: Pressure group after first dive
########################################################################

findPressureGroup = {} # dict that contains the minutes in the excel file for each depth
dfFindPressureGroup = pd.read_excel(dataPath, sheet_name='find pressure group (meter)')
keysInFindPressureGroup = []
for i,column_name in enumerate(dfFindPressureGroup): #iterates through depths, i.e. 10 m, 12 m, ...
    if i == 0: # first columns contains the new pressure group that we are interested in
        pressureGroup = dfFindPressureGroup[column_name]
    else: # other columns contain the depth at which we are
        key = float(f'{float(column_name):1.02f}') # round the value because it has many digits in the excel file
        keysInFindPressureGroup.append(key) 
        findPressureGroup[key] = dfFindPressureGroup[column_name]
keysInFindPressureGroup.sort(reverse=True) 




########################################################################
# reading in data from table 2: Pressure group after surface interval
########################################################################

pressureGroupAfterSurfaceInterval = pd.read_excel(dataPath, sheet_name='get new pressure group')
mappingSurfaceTimeToNewPgroup = {} 
listmappingSurfaceTimeToNewPgroup = []
indexToPressureGroup = {}
for i,oldPGroup in enumerate(pressureGroupAfterSurfaceInterval['pressure group from table 1 new pressure group']):
    if not pd.isnull(oldPGroup):
        listmappingSurfaceTimeToNewPgroup.append(oldPGroup)
        indexToPressureGroup[i] = oldPGroup
        indexToPressureGroup[i+1] = oldPGroup
        mappingSurfaceTimeToNewPgroup[oldPGroup] = {}

for i,column_name in enumerate(pressureGroupAfterSurfaceInterval):
    if i == 0: #skip first row
        continue
    for j in range(len(pressureGroupAfterSurfaceInterval)):
        if j % 2 != 0: #skips every second row because of the layout of the excel file
            continue
        if not pd.isnull(pressureGroupAfterSurfaceInterval[column_name].iloc[j]):
            mappingSurfaceTimeToNewPgroup[indexToPressureGroup[j]][pressureGroupAfterSurfaceInterval[column_name].iloc[j]] = column_name





########################################################################
# reading in data from table 3: Maximum bottom time at desired depth
########################################################################

dfBottomTimeSecondDive = pd.read_excel(dataPath, sheet_name='max bottom time 2nd dive')
residualNitrogenTime = {}
maxBottomTime = {}
oldPressureGroupInBottomTime = []
depthsfor2ndDive = []
indexBottomTime = {}
indexResNitrogen = {}
for i,keyPG in enumerate(dfBottomTimeSecondDive): # iterate through Z Y X W ...
    if i > 0: # first column contains the depths and it is not a key of interest
        oldPressureGroupInBottomTime.append(keyPG)
        maxBottomTime[keyPG] = {}
        residualNitrogenTime[keyPG] = {}
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


##############################
# creating random dive profile
##############################

# start at surface
depth = [0]
time = [0]

# choose first bottom time
depthNp = np.random.randint(-42,-10, 1).tolist()
# limit maximum time at bottom to whatever is allowed according to the table

key = getKeyForDepth(depthNp[0])
timeNp = np.random.randint(3,getmaxTime1stDive(key), 1).tolist()
surfaceTime = np.random.randint(10,70,1).tolist()
maxDepthSecondDive = depthNp[0]

# limit first bottom time to maximum first depth. 
depthSecondDive = np.random.randint(maxDepthSecondDive,-10, 1).tolist()

# add bottom time
for i in range(2):
    depth.append(depthNp[0])

# add surface time
for i in range(2):
    depth.append(0)

# add second bottom time
for i in range(2):
    depth.append(depthSecondDive[0])

# go to surface again
depth.append(0)

# estimate that changes in depths happen within one minute
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

depthAndTime = dataForDiveComputerDepthTime
desiredDepth2ndDive = depthSecondDive


key = getKeyForDepth(depthAndTime[0][0])
oldPG = getPressureGroup(key,depthAndTime[0][1])
if depthAndTime[1][1] > 59:
    hour, minutes= divmod(depthAndTime[1][1], 60)
else:
    hour = 0
    minutes = depthAndTime[1][1]

surfaceTime = datetime.time(hour,minutes)




currentPG = getPressureGrAfterSurfaceIntervall(oldPG, surfaceTime)
maximumBottomTime, time, resN2Time = getMaxBottomTime(currentPG, desiredDepth2ndDive)
PG3 = getPressureGroupAfter2ndDive(maximumBottomTime, resN2Time)
filename = f'divingprofile_{depthAndTime[0][0]}'
visualizeDivingProfile(time,depth, filename)
writeDataForDivingComputer(depthAndTime, filename)


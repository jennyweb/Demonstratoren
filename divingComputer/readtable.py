import pandas as pd
import os
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(497)



        
def getMaxTimeFirstDive(key):
    i = 0
    while not np.isnan(findPressureGroup[key][i]):
        i += 1
    return findPressureGroup[key][i-1]
        


# visualization of dive profile and pressure groups
def visualizeDivingProfile(time, depth, filename):    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(time, depth, color = 'green', lw=2)
    plt.title(filename)
    plt.xlabel('time in min')
    plt.ylabel('depth in m')
    ax.annotate(f'PG1 = {pressureGroupAfterFirstDive}', xy=(time[2], 0.25), color= 'blue')
    ax.annotate(f'PG2 = {pressureGroupAfterSurfaceInterval}', xy=(time[4]-3,0.25), color= 'blue')
    ax.annotate(f'PG3 = {PG3}', xy=(time[6]-3,0.25), color= 'blue')
    ax.annotate(f'BT = {dataForDiveComputerDepthTime[0][1]} min', xy=(time[1]+1,depth[1]+0.25), color= 'orange')
    ax.annotate(f'ST = {dataForDiveComputerDepthTime[1][1]} min', xy=(time[4]/2,depth[3]+0.25), color= 'orange')
    ax.annotate(f'BT = {int(maximumBottomTime)} min', xy=(time[5]+1,depth[5]+0.25), color= 'orange')
    plt.savefig(os.path.join(currentWorkingDir, f'{filename}.png'))
    plt.close()






def createDepthProfile(depthNp, depthSecondDive):
    depth = [0]
    # add bottom time
    for _ in range(2):
        depth.append(depthNp)

    # add surface time
    for _ in range(2):
        depth.append(0)

    # add second bottom time
    for _ in range(2):
        depth.append(depthSecondDive)

    # go to surface again
    depth.append(0)
    return depth


def createTimeProfile(timeNp, surfaceTime):

    # start at surface
    time = [0]

    # estimate that changes in depths happen within one minute
    time.append(time[-1]+1)
    time.append(timeNp+time[-1])

    time.append(time[-1]+1)
    time.append(time[-1]+surfaceTime)
    time.append(time[-1]+1)

    return time


def combineProfiles(depthProfile, timeProfile):
    dataForDiveComputerDepthTime = []
    for i in range(2,len(timeProfile)):
        if i % 2 == 0:
            dataForDiveComputerDepthTime.append((depthProfile[i],(timeProfile[i]-timeProfile[i-1])))
    return dataForDiveComputerDepthTime


def getSurfaceTimeAsDatetimeObject(surfaceTime):
    if surfaceTime > 59:
        hour, minutes = divmod(surfaceTime, 60)
    else:
        hour = 0
        minutes = surfaceTime
    return datetime.time(hour,minutes)


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


def getKeyForDepth(depth):
    if depth > keysInFindPressureGroup[0]:
        raise RuntimeError (f'please make sure that the depth does not exceed 42m. I got {depth}')
        
    for i in range(len(keysInFindPressureGroup)):
        if abs(depth) >= keysInFindPressureGroup[i]:
            key = keysInFindPressureGroup[i-1]
            return key
    return keysInFindPressureGroup[-1]

assert getKeyForDepth(-30) >= 30., 'key extraction failed'


def getPressureGroup(key,time):
    minutesInCertainDepth = findPressureGroup[key]
    for i in range(len(minutesInCertainDepth)):
        if minutesInCertainDepth[i] >= time:
            return pressureGroup[i]

assert getPressureGroup(30.48,17) == 'L', 'Mapping of bottom time to pressure group failed'



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


def getPressureGroupAfterSurfaceInterval(oldPG, surfaceTime, mappingSurfaceTimeToNewPgroup):
    adequateTimeInterval = 0
    timezones = list(mappingSurfaceTimeToNewPgroup[oldPG].keys())
    timezones.sort()
    for i in range(len(timezones)):
        if surfaceTime < timezones[i]:
            adequateTimeInterval = timezones[i-1]
            break
    return mappingSurfaceTimeToNewPgroup[oldPG][adequateTimeInterval]

assert getPressureGroupAfterSurfaceInterval('L', getSurfaceTimeAsDatetimeObject(42), mappingSurfaceTimeToNewPgroup) == 'F', 'Mapping of initial pressure group to new pressure group after surface interval failed'



########################################################################
# reading in data from table 3: Maximum bottom time at desired depth
########################################################################

dfBottomTimeSecondDive = pd.read_excel(dataPath, sheet_name='max bottom time 2nd dive')
residualNitrogenTime = {}
maxBottomTime = {}
depthsForSecondDive = []
for i, keyPG in enumerate(dfBottomTimeSecondDive): # iterate through Z Y X W ...
    if i > 0: # first column contains the depths and it is not a key of interest
        maxBottomTime[keyPG] = {} # initiate with empty dictionary 
        residualNitrogenTime[keyPG] = {} # initiate with empty dictionary

for i, depth2ndDive in enumerate(dfBottomTimeSecondDive['depth in m pressure group at the end of surface intervall']): # iterate over first column
    if not pd.isnull(depth2ndDive):
        depth2ndDive = float(f'{float(depth2ndDive):1.02f}') # round 
        depthsForSecondDive.append(depth2ndDive)

depthsForSecondDive.sort()
for i, column_name in enumerate(dfBottomTimeSecondDive):
    if i == 0:
        continue

    for j in range(0,len(depthsForSecondDive)):
        if not pd.isnull(dfBottomTimeSecondDive[column_name].iloc[j*2]):
            residualNitrogenTime[column_name][depthsForSecondDive[j]] = dfBottomTimeSecondDive[column_name].iloc[j*2]
        if not pd.isnull(dfBottomTimeSecondDive[column_name].iloc[j*2+1]):
            maxBottomTime[column_name][depthsForSecondDive[j]] = dfBottomTimeSecondDive[column_name].iloc[j*2+1]


def updateTimeProfile(timeProfile, maximumBottomTime):
    timeProfile.append(int(timeProfile[-1]+maximumBottomTime))
    timeProfile.append(timeProfile[-1]+1)


def getMaxBottomTimeAndMaximumNitrogenResidual(currentPressureGroup, desiredDivingDepth):
    for i in range(len(depthsForSecondDive)):
        if abs(desiredDivingDepth) < depthsForSecondDive[i]:
            key = depthsForSecondDive[i]
            break
    maximumBottomTime = maxBottomTime[currentPressureGroup][key]
    resN2Time = residualNitrogenTime[currentPressureGroup][key]
    return maximumBottomTime, resN2Time


assert getMaxBottomTimeAndMaximumNitrogenResidual('N', 25) == (3.0, 22.0), 'Extraction of maximum bottom time and residual nitrogen failed'


def getPressureGroupAfter2ndDive(maximumBottomTime, resN2Time):
    totalBottomTime = maximumBottomTime + resN2Time
    key2ndDive = getKeyForDepth(depthSecondDive)
    PG3 = getPressureGroup(key2ndDive,totalBottomTime)
    return PG3


##############################
# creating random dive profile
##############################

# choose first bottom time
depthFirstDive = np.random.randint(-42,-10, 1).tolist()[0] # yields -30

# limit maximum time at bottom to whatever is allowed according to the table
key = getKeyForDepth(depthFirstDive)
maxTimeFirstDive = int(getMaxTimeFirstDive(key))
bottomTimeFirstDive = np.random.randint(3,maxTimeFirstDive, 1).tolist()[0]
surfaceTime = np.random.randint(10,70,1).tolist()[0]
maxDepthSecondDive = depthFirstDive

# limit first bottom time to maximum first depth. 
depthSecondDive = np.random.randint(maxDepthSecondDive,-10, 1).tolist()[0]


depthProfile = createDepthProfile(depthFirstDive, depthSecondDive)
timeProfile = createTimeProfile(bottomTimeFirstDive, surfaceTime)
dataForDiveComputerDepthTime = combineProfiles(depthProfile, timeProfile)



##############################
# derive the pressure groups
##############################

pressureGroupAfterFirstDive = getPressureGroup(key,dataForDiveComputerDepthTime[0][1])
surfaceTimeDatetimeObject = getSurfaceTimeAsDatetimeObject(dataForDiveComputerDepthTime[1][1])
pressureGroupAfterSurfaceInterval = getPressureGroupAfterSurfaceInterval(pressureGroupAfterFirstDive, surfaceTimeDatetimeObject, mappingSurfaceTimeToNewPgroup)

maximumBottomTime, resN2Time = getMaxBottomTimeAndMaximumNitrogenResidual(pressureGroupAfterSurfaceInterval, depthSecondDive)
updateTimeProfile(timeProfile,maximumBottomTime)
PG3 = getPressureGroupAfter2ndDive(maximumBottomTime, resN2Time)
visualizeDivingProfile(timeProfile, depthProfile, 'divingProfile')


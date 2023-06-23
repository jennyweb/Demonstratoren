import pandas as pd
import os
import csv
import datetime

currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, 'diveTableMeters.xlsx')

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

depthAndTime = [(-34, 13), (0, 42), (-28, 8)]

depth = depthAndTime[0][0]
time = depthAndTime[0][1]

def getKeyForDepth(depth):
    if depth > keysInFindPressureGroup[0]:
        raise RuntimeError (f'please make sure that the depth does not exceed 42m. I got {depth}')
        
    for i in range(len(keysInFindPressureGroup)):
        if abs(depth) >= keysInFindPressureGroup[i]:
            key = keysInFindPressureGroup[i-1]
            return key
    return keysInFindPressureGroup[-1]
    

key = getKeyForDepth(depth)

def getPressureGroup(key,time):
    pressureGroupforTt = None
    minutesInCertainDepth = findPressureGroup[key]
    for i in range(len(minutesInCertainDepth)):
        if minutesInCertainDepth[i] >= time:
            pressureGroupforTt = pressureGroup[i]
            return pressureGroupforTt
   
# print(getPressureGroup(key,time))


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

# columnInTable = pressureGroupAfterSurfaceIntervall[column_name]
for i,column_name in enumerate(pressureGroupAfterSurfaceIntervall):
    if i == 0: #skip first row
        continue
    for j in range(len(pressureGroupAfterSurfaceIntervall)):
        if j % 2 != 0: #skips everysecond row because of time intervall
            continue
        if not pd.isnull(pressureGroupAfterSurfaceIntervall[column_name].iloc[j]):
            mappingSurfaceTimeToNewPgroup[indexToPressureGroup[j]][pressureGroupAfterSurfaceIntervall[column_name].iloc[j]] = column_name

oldPG = getPressureGroup(key,time)
print(oldPG) 
surfaceTime = datetime.time(0, 30)
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
dfBottomTimeSecondDive = pd.read_excel(dataPath, sheet_name='max bottom time 2nd dive')
residualNitrogenTime = {}
maxBottomTime = {}
oldPGInBottomTime = []
depthsfor2ndDive = []
for i,column_name in enumerate(dfBottomTimeSecondDive):
    if i > 0:
        keyPG = column_name
        oldPGInBottomTime.append(keyPG)
for i,depth2ndDive in enumerate(dfBottomTimeSecondDive['depth in m pressure group at the end of surface intervall']):
    if not pd.isnull(depth2ndDive):
        depth2ndDive = float(f'{float(depth2ndDive):1.02f}')
        depthsfor2ndDive.append(depth2ndDive)

# for i in range(len())


print(keysInBottomTime, depthsfor2ndDive)


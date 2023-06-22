import pandas as pd
import os
import csv

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

from datetime import datetime
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
    if i == 0:
        continue
    for j in range(len(pressureGroupAfterSurfaceIntervall)):
        if not pd.isnull(pressureGroupAfterSurfaceIntervall[column_name].iloc[j]):
            print(column_name)
            mappingSurfaceTimeToNewPgroup[indexToPressureGroup[j]] = {str(pressureGroupAfterSurfaceIntervall[column_name].iloc[j]):column_name}


print(mappingSurfaceTimeToNewPgroup)
    



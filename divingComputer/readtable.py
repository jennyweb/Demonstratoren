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

pressureGroupAfterSurfaceIntervall = pd.read_excel(dataPath, sheet_name='get new pressure group')
pressureGroup1stDive = {}
listPressureGroup1stDive = []
print(pressureGroupAfterSurfaceIntervall[ 'pressure group from table 1 new pressure group'])
for i in pressureGroupAfterSurfaceIntervall[ 'pressure group from table 1 new pressure group']:
    if pressureGroupAfterSurfaceIntervall[ 'pressure group from table 1 new pressure group'] !='NaN':
        listPressureGroup1stDive.append(pressureGroupAfterSurfaceIntervall[ 'pressure group from table 1 new pressure group'][i])
print(listPressureGroup1stDive)
    



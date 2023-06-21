import pandas as pd
import os

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

T = -15
t = 12
def getKeyForDepth(T):
    if T > keysInFindPressureGroup[0]:
        raise RuntimeError (f'please make sure that the depth does not exceed 42m. I got {T}')
    
        
    for i in range(len(keysInFindPressureGroup)):
        if abs(T) > keysInFindPressureGroup[i]:
            key = keysInFindPressureGroup[i-1]
            return key
    return keysInFindPressureGroup[-1]

key = getKeyForDepth(T)

def getPressureGroup(key,t):
    pressureGroupforTt = None
    minutesInCertainDepth = findPressureGroup[key]
    for i in range(0,len(minutesInCertainDepth)):
        if minutesInCertainDepth[i] > t:
            print(minutesInCertainDepth[i])
            pressureGroupforTt = pressureGroup[i-1]
    return pressureGroupforTt
   
print(getPressureGroup(key,t))
    



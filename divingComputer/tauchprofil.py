import csv
import matplotlib.pyplot as plt
import numpy as np
import os

currentWorkingDir = os.path.dirname(__file__)

def getDiveProfile(x): 
    depth = [0]
    time = [0]
    depthNp = np.random.randint(-42,-10, size=x).tolist()
    timeNp = np.random.randint(5,15, size=x).tolist()
    for i in range(len(depthNp)):
        depth.append(depthNp[i])
        depth.append(depthNp[i])
    for i in range(len(timeNp)):
        time.append(time[-1]+1)
        time.append(timeNp[i]+time[-1])
    maxDepth = min(depth)
    filename = f'divingprofile_{maxDepth}'
    visualizeDivingProfile(time,depth, filename)
    dataForDiveComputerDepthTime = []
    for i in range(len(timeNp)):
        dataForDiveComputerDepthTime.append((depthNp[i],timeNp[i]))
    writeDataForDivingComputer(dataForDiveComputerDepthTime, filename)
    return dataForDiveComputerDepthTime
    
def visualizeDivingProfile(time,depth,filename):    
    plt.plot(time,depth)
    plt.title(filename)
    plt.xlabel('time in s')
    plt.ylabel('depth in m')
    plt.savefig(os.path.join(currentWorkingDir, f'{filename}.png'))
    plt.close()

def writeDataForDivingComputer(dataForDiveComputerDepthTime,filename):
    with open(os.path.join(currentWorkingDir, f'{filename}.txt'),'w') as fout:
        fout.write('depth time\n')
        for i in range(len(dataForDiveComputerDepthTime)):
            fout.write(f'{dataForDiveComputerDepthTime[i]}\n')
    

print(getDiveProfile(3))



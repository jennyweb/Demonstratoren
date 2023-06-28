import csv
import matplotlib.pyplot as plt
import numpy as np
import os

currentWorkingDir = os.path.dirname(__file__)
np.random.seed(4297)

def getDiveProfile(): 
    depth = [0]
    time = [0]
    depthNp = np.random.randint(-42,-10, 1).tolist()
    timeNp = np.random.randint(5,40, 1).tolist()
    surfaceTime = np.random.randint(10,70,1).tolist()
    maxDepthSecondDive = depthNp[0]
    depthSecondDive = np.random.randint(maxDepthSecondDive,-10, 1).tolist()
    timeNpSecondDive = np.random.randint(5,30, 1).tolist()
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
    time.append(timeNpSecondDive[0]+ time[-1])
    time.append(time[-1]+1)

    maxDepth = min(depth)
    
    filename = f'divingprofile_{maxDepth}'
    visualizeDivingProfile(time,depth, filename)
    dataForDiveComputerDepthTime = []
    for i in range(2,len(time)):
        if i % 2 == 0:
            dataForDiveComputerDepthTime.append((depth[i],(time[i]-time[i-1])))
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
    

print(getDiveProfile(1))



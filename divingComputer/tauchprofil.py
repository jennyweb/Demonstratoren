import csv
import matplotlib.pyplot as plt
import numpy as np

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
    print(time, timeNp)
    filename = f'divingprofile_{maxDepth}'
    visualizeDivingProfile(time,depth, filename)
    
def visualizeDivingProfile(time,depth,filename):    
    plt.plot(time,depth)
    plt.title(filename)
    plt.xlabel('time')
    plt.ylabel('depth')
    plt.savefig(f'DivingComputer\{filename}.png')
    plt.close()


print(getDiveProfile(3))



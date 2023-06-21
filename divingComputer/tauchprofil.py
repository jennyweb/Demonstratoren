import csv
import matplotlib.pyplot as plt
import numpy as np

def getDiveProfile(x): 
    depth = [0]
    time = [0]
    depthNp = np.random.randint(10,42, size=x).tolist()
    timeNp = np.random.randint(5,15, size=x).tolist()
    for i in range(len(depthNp)):
        depth.append(depthNp[i])
        depth.append(depthNp[i])
        time.append(time[-1]+1)
        time.append(timeNp[i])
    print(depth,time)

    # filename = f'divingprofile_{depth}'
    # with open(f'DivingComputer\{filename}.txt', 'w') as fout:
    #     fout.write('time\tdepth\n')
     
        #         currentDepth = depth
        #         fout.write(f'{currentTime}\t{currentDepth}\n')
    # time = []
    # depth = []
    # with open(f'DivingComputer\{filename}.txt', 'r') as fin:
    #     for line in csv.DictReader(fin, delimiter='\t'):
    #         time.append(line['time'])
    #         depth.append(float(line['depth']))
    # visualizeDivingProfile(time,depth, filename)
    
# def visualizeDivingProfile(time,depth,filename):    
#     plt.plot(time, depth)
#     plt.title(filename)
#     plt.xlabel('time')
#     plt.ylabel('depth')
#     plt.savefig(f'DivingComputer\{filename}.png')
#     plt.close()


print(getDiveProfile(3))



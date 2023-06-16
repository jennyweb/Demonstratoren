import csv
import pandas as pd
import matplotlib.pyplot as plt
import os

currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, 'givenData.dat')

with open(dataPath,'r') as fin:
    time = []
    velocity = []
    distance = []
    for line in fin:
        if line.startswith('time'):
            continue
        # line = line.strip()
        df = line.strip().split(' ')
        time.append(float(df[0]))
        velocity.append(float(df[1]))
        distance.append(float(df[2]))

with open(dataPath,'r') as fin:
    time = []
    velocity = []
    distance = []
    for line in csv.DictReader(fin,delimiter=' '):
        time.append(float(line['time']))
        velocity.append(float(line['velocity']))
        distance.append(float(line['distance']))
    # dt = []
    # for i in range(len(time)-1):
    #     dt.append(time[i+1]-time[i])
    dt = time[1] - time[0]
    distance_calc = []
    distance_sum = []
    for i in range(len(velocity)):
        distance_calc.append(velocity[i]*dt)
    for i in range(1,len(distance_calc)):
        distance_calc[i] += distance_calc[i-1]


    plt.plot(time,distance_calc, label='Calculated Distance', linewidth=3, color='green')
    plt.plot(time, distance, label='Reference Data', linestyle='dashed', color = 'orange')
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('distance')
    plt.savefig(f'{currentWorkingDir}\calc-distanceVSgiven-distance.png')
    plt.close()

    # plt.subplot(1,2,1)
    # plt.plot(time, distance_calc)
    # plt.title('Calculated Distance')
    # plt.xlabel('time')
    # plt.ylabel('distance')
   
    # plt.subplot(1,2,2)
    # plt.plot(time, distance) 
    # plt.title('Reference Data')
    # plt.xlabel('time')
    # plt.ylabel('distance')
    # plt.savefig(f'{currentWorkingDir}\Subplot.png')
    # plt.close()

df = pd.read_csv(dataPath, delimiter=' ')

for i in range(len(df['time'])-1):
    dt = df['time'].iloc[i+1] - df['time'].iloc[i]
    # print(dt)
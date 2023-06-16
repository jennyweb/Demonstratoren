import csv
import pandas as pd
import matplotlib.pyplot as plt


with open('workingWithGivenData\givenData.dat','r') as fin:
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
    # print(time)


with open('workingWithGivenData\givenData.dat','r') as fin:
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

    calc_distance = plt.figure(figsize=(6, 6))
    plt.plot(time, distance_calc)
    plt.title('Calculated Distance')
    plt.xlabel('time')
    plt.ylabel('distance')
    calc_distance.savefig('workingWithGivenData\calculated_distance.png', dpi=calc_distance.dpi)
   
    ref = plt.figure(figsize=(6, 6))
    plt.plot(time, distance) 
    plt.title('Reference Data')
    plt.xlabel('time')
    plt.ylabel('distance')
    ref.savefig('workingWithGivenData\givenData.png', dpi=ref.dpi)

df = pd.read_csv('workingWithGivenData\givenData.dat', delimiter=' ')


for i in range(len(df['time'])-1):
    dt = df['time'].iloc[i+1] - df['time'].iloc[i]
    # print(dt)
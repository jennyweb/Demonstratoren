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
    # plt.plot(time, distance_calc)
df = pd.read_csv('workingWithGivenData\givenData.dat', delimiter=' ')


for i in range(len(df['time'])-1):
    dt = df['time'].iloc[i+1] - df['time'].iloc[i]
    # print(dt)
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
df = pd.read_csv('workingWithGivenData\givenData.dat', delimiter=' ')


for i in range(len(df['time'])-1):
    dt = df['time'].iloc[i+1] - df['time'].iloc[i]
    # print(dt)
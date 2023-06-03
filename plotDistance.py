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

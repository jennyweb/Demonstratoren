import csv
import matplotlib.pyplot as plt

def getDiveProfile(depth): 
    currentDepth = 0
    filename = f'divingprofile_{depth}'
    with open(f'DivingComputer\{filename}.txt', 'w') as fout:
        fout.write('time\tdepth\n')
        for i in range(240):
            currentTime = i * 10
            if currentDepth > depth:
                if currentTime % 4 == 0:
                    currentDepth = currentDepth
                else:
                    currentDepth -= i * 0.3
                    currentDepth = max(currentDepth, depth)
                fout.write(f'{currentTime}\t{currentDepth}\n')
            else: 
                currentDepth = depth
                fout.write(f'{currentTime}\t{currentDepth}\n')
    time = []
    depth = []
    with open(f'DivingComputer\{filename}.txt', 'r') as fin:
        for line in csv.DictReader(fin, delimiter='\t'):
            time.append(line['time'])
            depth.append(float(line['depth']))
    visualizeDivingProfile(time,depth, filename)
    
def visualizeDivingProfile(time,depth,filename):    
    plt.plot(time, depth)
    plt.title(filename)
    plt.xlabel('time')
    plt.ylabel('depth')
    plt.savefig(f'DivingComputer\{filename}.png')
    plt.close()


getDiveProfile(-13)
getDiveProfile(-18)
getDiveProfile(-25)
getDiveProfile(-30)
getDiveProfile(-37)


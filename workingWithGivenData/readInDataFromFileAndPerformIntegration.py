import csv
import pandas as pd
import matplotlib.pyplot as plt
import os

currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, "givenData.dat")

# mode 1: Reading file line by line
with open(dataPath, "r") as fin:
    time = []
    velocity = []
    distance = []
    for line in fin:
        if line.startswith("time"):
            continue
        # line = line.strip()
        df = line.strip().split(" ")
        time.append(float(df[0]))
        velocity.append(float(df[1]))
        distance.append(float(df[2]))

# mode 2: using csv DictReader to read file lines
with open(dataPath, "r") as fin:
    time = []
    velocity = []
    distance = []
    for line in csv.DictReader(fin, delimiter=" "):
        time.append(float(line["time"]))
        velocity.append(float(line["velocity"]))
        distance.append(float(line["distance"]))


# mode 3: using pandas to read file
df = pd.read_csv(dataPath, delimiter=" ")
time = df["time"]
velocity = df["velocity"]
distance = df["distance"]

# data of the file import is overwritten every time. Simply use the last one


# integrate data using a forward scheme
dt = time[1] - time[0]  # fixed dt in this case
distance_calc = []
for i in range(len(velocity)):
    distance_calc.append(velocity[i] * dt)
for i in range(1, len(distance_calc)):
    distance_calc[i] += distance_calc[i - 1]


# plot results
plt.plot(time, distance_calc, label="Calculated Distance", linewidth=3, color="green")
plt.plot(time, distance, label="Reference Data", linestyle="dashed", color="orange")
plt.legend(loc="upper right")
plt.xlabel("time $t$ in s")
plt.ylabel("distance $m$ in m")
plt.savefig(f"{currentWorkingDir}\calc-distanceVSgiven-distance.png")
plt.close()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy

currentWorkingDir = os.path.dirname(__file__)
picDir = os.path.join(currentWorkingDir, "pic")

if not os.path.isdir(picDir):
    os.mkdir(picDir)


class vector:
    def __init__(self, values) -> None:
        self.values = values

    def __len__(self):
        return len(self.values)

    def __sub__(self, other):
        if len(self.values) != len(other.values):
            return "unable to perform subtraction"
        new_vector = []
        for i in range(len(self.values)):
            new_vector.append(self.values[i] - other.values[i])
        return vector(new_vector)

    def __add__(self, other):
        if len(self.values) != len(other.values):
            return "unable to perform subtraction"
        new_vector = []
        for i in range(len(self.values)):
            new_vector.append(self.values[i] + other.values[i])
        return vector(new_vector)

    def __getitem__(self, i):
        return self.values[i]

    def __mul__(self, factor):
        scalar = 0
        if isinstance(factor, vector):
            if len(self.values) != len(factor.values):
                raise RuntimeError("unable to perform vector multiplication")
            for i in range(len(self.values)):
                scalar += self.values[i] * factor.values[i]
                return scalar
        else:
            new_vector = []
            for i in range(len(self.values)):
                new_vector.append(self.values[i] * factor)
            return vector(new_vector)

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def slope(self):
        return self.values[0] / self.values[1]

    def getOrthogonalVector(self):
        m = self.slope()
        deltaY = 1
        deltaX = -1 * m * deltaY
        return vector([deltaX, deltaY])

    def vectorLength(self):
        sumSquare = 0
        for i in range(len(self.values)):
            sumSquare += (self.values[i]) ** 2
        return np.sqrt(sumSquare)

    def __repr__(self):
        return f"[{self.values[0]} {self.values[1]}]"


currentWorkingDir = os.path.dirname(__file__)
dataPath = os.path.join(currentWorkingDir, "sizeDistribution.xlsx")

df = pd.read_excel(dataPath, header=1)
sizeDistribution = []
volumeFrequency = []
accumulatedVolumeFrequency = []
for i in range(len(df["Größe (μm)"])):
    sizeDistribution.append(df["Größe (μm)"][i])
    volumeFrequency.append(df["% Volumen In"][i])
    accumulatedVolumeFrequency.append(df[df.columns[2]][i])

for i in range(len(accumulatedVolumeFrequency)):
    if accumulatedVolumeFrequency[i] == 100:
        xmax = sizeDistribution[i + 4]
        break
for i in range(len(accumulatedVolumeFrequency)):
    if accumulatedVolumeFrequency[i] != 0:
        xmin = sizeDistribution[i - 4]
        break


def computeLognormDistribution(µ, sigma):
    lognormDistribution = []
    for i in range(len(sizeDistribution)):
        x = (1.0 / (sigma * sizeDistribution[i] * np.sqrt(2 * np.pi))) * np.exp(
            -((np.log(sizeDistribution[i]) - µ) ** 2) / (2 * sigma**2)
        )
        lognormDistribution.append(x)

    lognormDistribution = np.array(lognormDistribution)
    lognormDistribution *= 100.0 / np.sum(lognormDistribution)

    return lognormDistribution


def getDeviation(argIn, imageCounter=0, drawImage=True):
    µ = argIn[0]
    sigma = argIn[1]

    lognormDistribution = computeLognormDistribution(µ, sigma)

    if drawImage == True:
        # compute scipy solution
        lognormScipySolution = computeLognormDistribution(µSciPy, sigmaScipy)
        plt.plot(sizeDistribution, volumeFrequency, color="blue", label="data")
        plt.plot(sizeDistribution, lognormDistribution, color="green", label="fit")
        plt.plot(sizeDistribution, lognormScipySolution, color="black", label="SciPy")
        plt.legend(loc="upper right")
        plt.xlim([xmin, xmax])
        plt.xlabel("size in µm")
        plt.ylabel("size distribution in %")
        plt.title(f"current sigma = {sigma:1.04f}, current µ = {µ:1.03f}")
        plt.savefig(
            os.path.join(currentWorkingDir, f"pic/Distribution-{imageCounter:04d}.png")
        )
        plt.close()

    deviation = 0
    for i in range(len(volumeFrequency)):
        deviation += abs(volumeFrequency[i] - lognormDistribution[i])
    return deviation


def interfaceToGetDeviation(argIn):
    return getDeviation(argIn, drawImage=False)


def isSorted(listA):
    for i in range(len(listA) - 1):
        if listA[i] > listA[i + 1]:
            return False
    return True


def nelderMead(func, x0):
    # create initial state. We need points u v w

    def orderByDeviation(func, p1, p2, p3):
        errorOfPs = []
        listOfPs = [p1, p2, p3]
        errorOfP1 = func(p1.values)
        errorOfP2 = func(p2.values)
        errorOfP3 = func(p3.values)
        errorOfPs.append(errorOfP1)
        errorOfPs.append(errorOfP2)
        errorOfPs.append(errorOfP3)

        while not isSorted(errorOfPs):
            for i in range(len(errorOfPs) - 1):
                if errorOfPs[i] > errorOfPs[i + 1]:
                    placeholderError = errorOfPs[i]
                    errorOfPs[i] = errorOfPs[i + 1]
                    errorOfPs[i + 1] = placeholderError
                    placeholderP = listOfPs[i]
                    listOfPs[i] = listOfPs[i + 1]
                    listOfPs[i + 1] = placeholderP

        u = listOfPs[0]
        v = listOfPs[1]
        w = listOfPs[2]

        return u, v, w

    p1 = vector(x0)
    p2 = vector([x0[0], x0[1] * 1.2])
    p3 = vector([x0[0] * 1.2, x0[1]])

    u, v, w = orderByDeviation(func, p1, p2, p3)

    for imageCounter in range(60):
        midPoint = u + (v - u) * 0.5

        potentialNewP = w + 2 * (midPoint - w)

        errorOfPotentialNewP = func(potentialNewP)
        if errorOfPotentialNewP < func(v) and errorOfPotentialNewP > func(u):
            w = v
            v = potentialNewP

        elif errorOfPotentialNewP < func(u):
            ExtendedPotentialNewP = w + 3 * (midPoint - w)

            if func(ExtendedPotentialNewP) < errorOfPotentialNewP:
                w = v
                v = u
                u = ExtendedPotentialNewP

            else:
                w = v
                v = u
                u = potentialNewP

        else:
            halfPoint1 = w + 0.5 * (midPoint - w)
            halfPoint2 = w + 1.5 * (midPoint - w)

            errorHalfPoint1 = func(halfPoint1)
            errorHalfPoint2 = func(halfPoint2)

            pointOfChoice = (
                halfPoint1 if errorHalfPoint1 < errorHalfPoint2 else halfPoint2
            )

            if func(pointOfChoice) < func(v) and func(pointOfChoice) > func(u):
                w = v
                v = pointOfChoice

            elif func(pointOfChoice) < func(u):
                w = v
                v = u
                u = pointOfChoice

            else:
                v = v + (u - v) * 0.5
                w = w + (u - w) * 0.5

        # make drawing of current progress for video
        getDeviation(u, imageCounter=imageCounter, drawImage=True)

    return u


# initial guess
sigma = 0.2
µ = np.log(40) - 0.5 * sigma**2

# retrieve scipy solution
resultSciPy = scipy.optimize.minimize(
    interfaceToGetDeviation, x0=[µ, sigma], method="Nelder-Mead"
)
µSciPy, sigmaScipy = resultSciPy.x[0], resultSciPy.x[1]

# use own algorithm
resultOwnNelderMead = nelderMead(interfaceToGetDeviation, x0=[µ, sigma])
µ, sigma = resultOwnNelderMead[0], resultOwnNelderMead[1]

print(f"Solution scipy: µ = {µSciPy:1.03e} sigma = {sigmaScipy:1.03e}")
print(f"Own algorithm : µ = {µ:1.03e} sigma = {sigma:1.03e}")

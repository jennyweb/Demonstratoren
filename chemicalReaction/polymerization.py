import numpy as np
import matplotlib.pyplot as plt

maxChainLength = 100
concentrations = np.zeros(maxChainLength)
concentrations[0] = 1
t = 0
dt = 1e-2
r = 0.01 # mol/s
imageCounter = 0
iteration = 0

def plotConcentration(concentrations):
    plt.plot(concentrations)
    plt.savefig(f'chemicalReaction/concentrationProfile-{imageCounter:04d}.png')
    plt.close()
    

while concentrations[0] > 1e-20:
    for i in range(maxChainLength,1,-1):
        concentrationRate =  r * concentrations[0] * concentrations[i-2] * dt #mol/l
        concentrationRateMonomer = concentrationRate/2
        concentrationRateShorterPolymer = concentrationRate/2
        concentrations[i-1] = concentrations[i-1] + concentrationRate
        concentrations[0] = concentrations[0] - concentrationRateMonomer
        concentrations[i-2] = concentrations[i-2] - concentrationRateShorterPolymer
        # works also for the Dimer, because for P2, there is i == 2 -> i-2 = 0, hence the Monomer is substracted twice and the concentrationRate is building up on the monomerconcentration to the power of 2
    print(concentrations[0])
    if iteration % 50 == 0:
        plotConcentration(concentrations)
        imageCounter += 1
    iteration += 1
    t += dt




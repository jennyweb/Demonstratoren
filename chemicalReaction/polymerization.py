import numpy as np
import matplotlib.pyplot as plt
import os, shutil
from scipy.integrate import odeint
from alive_progress import alive_bar

maxChainLength = 15
concentrations = np.zeros(maxChainLength)
concentrations[0] = 1
t = 0
dt = 1e-2
r = 0.01 # L/(mol s)
iteration = 0

# create folder into which data will be written 
currentWorkingDir = os.path.dirname(__file__)
picDir = os.path.join(currentWorkingDir, 'pic')

if os.path.isdir(picDir):
    shutil.rmtree(picDir)
os.mkdir(picDir)

def plotConcentration(concentrations, concentrationNumpy, imageCounter, t):
    plt.plot(list(range(1,maxChainLength+1)),concentrations, zorder=2, label='Simulation', linewidth=3, color='green')
    plt.plot(list(range(1,maxChainLength+1)),concentrationNumpy, zorder=2, label='Numpy Solution', linestyle='dashed', color = 'orange')
    plt.legend(loc='upper right')
    plt.xlabel('chain length')
    plt.xlim([0,15])
    plt.ylabel('concentration [mol/L]')
    plt.xticks([1,2,3,4,6, 8,10,12,14], ['Mon','Di','Tri',4,6,8,10,12,14])
    plt.title(f'$t$ = {t:1.01f} s')
    plt.axhline(color='grey', zorder=1, lw=0.5)
    plt.savefig(os.path.join(picDir,f'concentrationProfile-{imageCounter:04d}.png'))
    plt.close()

def getTotalMolarMass(conc):
    """
    concentrations[0] -> Monomer concentration, only 1 M
    concentrations[1] -> Dimer concentration, 2 M
    concentrations[2] -> Trimer concentration, 3 M
    """
    totalConc = 0.
    for i in range(len(conc)):
        molarMassFactor = i+1
        totalConc += molarMassFactor * conc[i]
    return totalConc


initialConcMon = getTotalMolarMass(concentrations)
# print(f'Initial concentration before reaction: {initialConcMon:1.02f} mol/L')
timepointsToBeUsedForNumpy = []

endConcentrationToBeReached = 1e-4

print('start own simulation')
concentrationPerTimeStamp = []
with alive_bar(manual=True) as bar:
    while concentrations[0] > endConcentrationToBeReached:

        concentrationRates = np.zeros(maxChainLength)

        for i in range(2, maxChainLength+1):

            # starts with i == 2 -> look at the dimer
            # works also for the Dimer, because for P2, there is i == 2 -> i-2 = 0, hence the Monomer is subtracted twice and the concentrationRate is building up on the monomer concentration to the power of 2

            # concentration rate according to differential equation
            concRate =  r * concentrations[0] * concentrations[i-2] # mol/(L s)

            # increase polymer concentration
            concentrationRates[i-1] +=  concRate

            # decrease monomer concentration
            concentrationRates[0] -= concRate

            # decrease concentration of the smaller polymer
            concentrationRates[i-2] -= concRate

        concentrations += concentrationRates * dt
        
        if iteration % 250 == 0:
            timepointsToBeUsedForNumpy.append(t)
            concentrationPerTimeStamp.append(concentrations.tolist())

        # increase counter
        iteration += 1
        t += dt

        # update progress bar
        simulationProgress = -1/(1-endConcentrationToBeReached)*(concentrations[0]-1)
        bar(simulationProgress)

finalAmountOfSubstance = getTotalMolarMass(concentrations)
# print(f'Final amount of substance after reaction: {finalAmountOfSubstance:1.02f} mol/L')

assert abs(finalAmountOfSubstance - initialConcMon) < 1e-3, "There has been a loss or gain of mass during the simulation"

print('Finished own simulation successfully')

# ### NUmpy solution
concentrationNP = []
for i in range(maxChainLength):
    concentrationNP.append(0)
concentrationNP[0] = 1
r = 0.01 # L/(mol s)

def DGL(concentrationNP, t):
    concentrationChange = []
    for i in range(maxChainLength):
        concentrationChange.append(0)
    r = 0.01 # L/(mol s)
    for i in range(2,len(concentrationNP)):
        concRate =  r * concentrationNP[0] * concentrationNP[i-2] # mol/(L s)

        # increase polymer concentration
        concentrationChange[i-1] +=  concRate

        # decrease monomer concentration
        concentrationChange[0] -= concRate

        # decrease concentration of the smaller polymer
        concentrationChange[i-2] -= concRate
    
    return concentrationChange


print('start numpy simulation')
y = odeint(DGL,concentrationNP, timepointsToBeUsedForNumpy)


print('Start plotting')
with alive_bar(len(concentrationPerTimeStamp)) as bar:
    for i in range(len(concentrationPerTimeStamp)):
        plotConcentration(concentrationPerTimeStamp[i], y[i], i, timepointsToBeUsedForNumpy[i])
        bar()

print('Finished script')
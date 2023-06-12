import numpy as np
import matplotlib.pyplot as plt
import os, shutil

maxChainLength = 15
concentrations = np.zeros(maxChainLength)
concentrations[0] = 1
t = 0
dt = 1e-2
r = 0.01 # L/(mol s)
imageCounter = 0
iteration = 0

# create folder into which data will be written 
currentWorkingDir = os.path.dirname(__file__)
picDir = os.path.join(currentWorkingDir, 'pic')

if os.path.isdir(picDir):
    shutil.rmtree(picDir)
    os.mkdir(picDir)
    

def plotConcentration(concentrations):
    plt.plot(list(range(1,maxChainLength+1)),concentrations, zorder=2)
    plt.xlabel('chain length')
    plt.xlim([0,15])
    plt.ylabel('concentration')
    plt.title(f'{t:1.01f} s')
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

while concentrations[0] > 1e-4:

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
    
    if iteration % 200 == 0:
        plotConcentration(concentrations)
        imageCounter += 1

    iteration += 1
    t += dt

finalAmountOfSubstance = getTotalMolarMass(concentrations)
# print(f'Final amount of substance after reaction: {finalAmountOfSubstance:1.02f} mol/L')

assert abs(finalAmountOfSubstance - initialConcMon) < 1e-3, "There has been a loss or gain of mass during the simulation"

print('Finished the simulation successfully')


import numpy as np
import matplotlib.pyplot as plt
import os, shutil
from scipy.integrate import odeint

maxChainLength = 15
concentrations = []
for i in range(maxChainLength):
    concentrations.append(0)
concentrations[0] = 1
r = 0.01 # L/(mol s)

def DGL(concentrations):
    concentrationChange = []
    for i in range(maxChainLength):
        concentrationChange.append(0)
    r = 0.01 # L/(mol s)
    for i in range(1,len(concentrations)):
        concRate =  r * concentrations[0] * concentrations[i-1] # mol/(L s)

        # increase polymer concentration
        concentrationChange[i] +=  concRate

        # decrease monomer concentration
        concentrationChange[0] -= concRate

        # decrease concentration of the smaller polymer
        concentrationChange[i-1] -= concRate
    
    return concentrationChange

concChange = DGL(concentrations)
chainLength = np.linspace(0,15)
y = odeint(concChange,concentrations,chainLength )


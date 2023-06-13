import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('fitEquationToData\sizeDistribution.xlsx', header=1)
size = []
volume = []
for i in range(len(df['Größe (μm)'])):
    size.append(df['Größe (μm)'][i])
    volume.append(df['% Volumen In'][i])



sigma = 0.2
µ = 40
p = []
for i in range(len(size)):
    x = (1/(sigma * size[i] * (2* np.pi)**0.5)) * np.exp(-((np.log(size[i])-µ)**2)/(2*sigma**2))
    p.append(x)
    print(max(p))

plt.plot(size, volume, 'b')
plt.plot(size, p, 'g')
plt.show()
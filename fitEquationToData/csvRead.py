import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('fitEquationToData\sizeDistribution.xlsx', header=1)
df.plot(x=df['Größe (μm)'], y=df['% Volumen In'],  kind='scatter')
plt.show()

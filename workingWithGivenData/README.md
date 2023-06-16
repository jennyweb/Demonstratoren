# Reading data and data integration
## Motivation

This projects demonstrates my skills to work with existing data. Data is given in a text file with three columns (time, velocity, and integrated distance). The goal is to integrate over the velocity. The third column is hence later used to verify the computation. 
## Setup
The steps executed in this script are the following:
- reading data using three methods: pure text import, pandas and the csv.DictReader model
- calculating the time interval d$t$ and the covered distance during d$t$
- accumulating the covered distance up to a given time
- plotting the calculated data using matplotlib and comparing it to the reference data
## Calculations

The distance $s$ is given by

$$
s(t) = \int_{t_i=0}^{t} v(t) \, \text{d}t \approx \sum_{i=0}^t v(t) \, \Delta t
$$


where $\Delta t = t_i - t_{i-1}$ using a backward scheme. 



# Result
The plot of the calculated distance is equal to the plot of the given data as shown in the following figure:
![Alt text](calc-distanceVSgiven-distance.png)

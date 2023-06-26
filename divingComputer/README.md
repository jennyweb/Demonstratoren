# Diving Computer
# Motivation
In this project the goal is to read in and work with data from .xlsx tables using pandas. The data is then used to calculate the maximum bottom time for the 2nd dive of one day at a given depths. Morover the residual nitrogen time is given (equals to the amout of time considered as already spent at a certain depth for the 2nd dive).

# Dive Theory

Dive tabels or computers are used to determine the time you can stay under water at a certain depth without the neccessity to make a decompression stop when heading back to the surface.
The pressure increases the deeper we dive and so does the absorbtion of nitrogen into the human body. The surface time is used to get rid of excessive nitrogen in the body and to minimize the rirk of decompression sickness.

The following table is used to determine the pressure group after the first dive of the day. The first row gives the maximum depth of the dive.
If the depth of the dive is not shown in the table, the next greater depth is used. The desired time at that depth can be found in the column below.
If the time is not shown, the next greater time is used for the calculation. Following the row to the left, we get the pressure group after the first dive.

![table1: pressure group after dive1](/divingComputer/Visualizations/table1.png)

When spending time at the surface the body gets rid of some of the excessive nitrogen in the blood and body tissue. To find out the pressure group after a certain time at the surface the following table is used. The first column shows the pressure group after the first dive. Following the corresponding row to the right until one finds the time spent at the surface, the corresponding column shows the new pressure group at the very top (pressure group after surface intervall).

![table2: pressure group after surface time](/divingComputer/Visualizations/table2SurfaceTime.png)


![table3: maximum bottom time after surface intervall](/divingComputer/Visualizations/table3MaxBottomTime.png)


give pressure group at the end of 2nd dive  = res N + bottom time 
table 1
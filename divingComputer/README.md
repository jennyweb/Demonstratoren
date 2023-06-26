# Diving Computer
# Motivation
In this project the goal is to read in and work with data from .xlsx tables using pandas. The data is then used to calculate the maximum bottom time for the 2nd dive of one day at a given depths. Morover the residual nitrogen time is given (equals to the amout of time considered as already spent at a certain depth for the 2nd dive).

# Dive Theory

Dive tabels or computers are used to determine the time you can stay under water at a certain depth without the neccessity to make a decompression stop when heading back to the surface.
The pressure increases the deeper we dive and so does the absorbtion of nitrogen into the human body. The surface time is used to get rid of excessive nitrogen in the body and to minimize the rirk of decompression sickness.


If the depth of your dive is not shown in the table, use the next greater depth.
If the time of your dive is not shown in the table, use the next greater time.

![table1: pressure group after dive1](/divingComputer/Visualizations/table1.png)

 to get rid of the excessive nitrogen in the blood and body tissue

![table2: pressure group after surface time](/divingComputer/Visualizations/table2SurfaceTime.png)


![table3: maximum bottom time after surface intervall](/divingComputer/Visualizations/table3MaxBottomTime.png)


give pressure group at the end of 2nd dive  = res N + bottom time 
table 1
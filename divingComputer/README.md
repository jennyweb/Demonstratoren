# Diving Computer
# Motivation
In this project the goal is to read in and work with data from .xlsx tables using pandas. The data is then used to calculate the maximum bottom time for the 2nd dive of one day at a given depths. Morover the residual nitrogen time is given (equals to the amout of time considered as already spent at a certain depth for the 2nd dive).

# Dive Theory

Dive tabels or computers are used to determine the time you can stay under water at a certain depth without the neccessity to make a decompression stop when heading back to the surface.
The pressure increases the deeper we dive and so does the absorbtion of nitrogen into the human body. The surface time is used to get rid of excessive nitrogen in the body and to minimize the rirk of decompression sickness.
# Table 1: Pressure group after first dive
The following table is used to determine the pressure group after the first dive of the day. The first row gives the maximum depth of the dive.
If the depth of the dive is not shown in the table, the next greater depth is used. The desired time at that depth can be found in the column below.
If the time is not shown, the next greater time is used for the calculation. Following the row to the left, we get the pressure group after the first dive. In the example the first dive is up to a depth of 30 meters for 19 min. According to table 1 this results in pressure group "N"

![table1: pressure group after dive1](/divingComputer/Visualizations/table1Ex.png)
# Table 2: Pressure group after surface intervall
When spending time at the surface the body gets rid of some of the excessive nitrogen in the blood and body tissue. To find out the pressure group after a certain time at the surface the following table is used. The first column shows the pressure group after the first dive , in our example this corresponds to pressure group "N". Following the corresponding row to the right until one finds the time spent at the surface, the corresponding column shows the new pressure group at the very top (pressure group after surface intervall). In our example the diver spends 42 min at the surface, so we pick the time interval of 37 min to 43 min. Following this column to the top gives the pressure group after the surface intervall in this case pressure group "G".

![table2: pressure group after surface time](/divingComputer/Visualizations/table2SurfaceTimeEx.png)
# Table 3: Maximum bottom time at desired depth
The following third table gives the maximum time one can spend at a desired depth. The first row shows the depths and the first column the pressure groups after the 1st dive (in this case group "G"). By finding the intersection of desired depth (25 meters in the example, so we pick the next higher number) and new pressure group one can find the maximum bottom time at that depth (bottom row) and the residual nitrogen time (top row). in our example the maximum bottom time is 12 min and the residual nitrogen time is 13 min.
By adding bottom time and  residual nitrogen time the  total bottom time can be calculated and the first table can be used again to calculate the pressure group after the 2nd dive. In our case the total bottom time is 25 min which lead to pressure group Q after the second dive to 25 meters.
![table3: maximum bottom time after surface intervall](/divingComputer/Visualizations/table3MaxBottomTimeEx.png)

# Example and Result
The following images shows a diving profile of a repetitive dive. On the first dive the diver reaches a depth of 30 m and stays there for 19 min. Resulting in  pressure group N (PG1 = N). She stays at the surface for 42 min which reduces her pressure group to G (PG2 = G). On the second dive the diver wants to dive to a depth of 25 m. The maximum time she can spend at this depth is 12 min which will result in pressure group Q (PG3 = Q).

![Alt text](/divingComputer/Visualizations/divingprofile_-30.png)
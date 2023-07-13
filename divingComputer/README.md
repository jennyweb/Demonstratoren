# Diving Computer
## Motivation
In this project the goal is to read in and work with data presented in an Excel file. The data is then used to calculate quantities of interest for dive planing, i.e. the maximum bottom time of a subsequent second dive within the same day and the maximum depth for that second dive. Another auxiliary variable commonly applied for dive tables is the so called pressure group that correspond to the nitrogen intake during the dive. When coming back to the surface, dissolved nitrogen in our body can create bubbles which can lead to sever injuries (ie. decompression sickness). The prevention of the bubble formation is hence focus of the dive planing. These pressure groups range from A to Z while the smaller the letter, the smaller the nitrogen intake. If a certain level of nitrogen intake is reached, we need to perform an extra safety stop for the nitrogen to slowly dissolve and being removed by simple breathing. 

The idea for this demonstartion evolved while doing the open water dive certification in Honduras. It was an exceptional experience, all of a sudden a whole new world opened up in front of my eyes. At the same it was scary as hell: taking out the regulator or even worse taking off the mask. 
Now, after being certified I can fully enjoy the laziest extreme sport on the planet (as my teacher said): Go down, don't get out of breath so swim as slow as you can, look at cool fish and go back up.

## Dive Theory
Dive tabels or computers are used to determine the time you can stay under water at a certain depth without the neccessity to make a decompression stop when heading back to the surface.
The pressure increases the deeper we dive and so does the absorbtion of nitrogen into the human body. The surface time is used to get rid of excessive nitrogen in the body and to minimize the rirk of decompression sickness.

## Table 1: Pressure group after first dive
The following table is used to determine the pressure group after the first dive of the day. The first row gives the maximum depth of the dive.
If the depth of the dive is not shown in the table, the next greater depth is used. The desired time at that depth can be found in the column below.
If the time is not shown, the next greater time is used for the calculation. Following the row to the left, we get the pressure group after the first dive. In the example the first dive is up to a depth of 30 meters for 17 min. According to table 1 this results in pressure group "L"
![table1: pressure group after dive1](/divingComputer/Visualizations/table1Ex.png)

## Table 2: Pressure group after surface intervall
While spending time at the surface, the body gets rid of excessive nitrogen in the blood and body tissue. Table 2 is used to determine the new pressure group after a certain time at the surface. The first column shows the pressure group after the first dive (in our example this corresponds to pressure group "L"). Following the corresponding row to the right until one finds the time spent at the surface, the corresponding column shows the new pressure group at the very top (pressure group after surface intervall). In our example, the diver spends 42 min at the surface, so we pick the time interval of 35 min to 42 min. Following this column to the top gives the pressure group after the surface intervall; in this case it leads to the pressure group "F".
![table2: pressure group after surface time](/divingComputer/Visualizations/table2SurfaceTimeEx.png)

## Table 3: Maximum bottom time at desired depth
The following third table gives the maximum time one can spend at a desired depth. The first row shows the depths and the first column the pressure groups after the 1st dive (in this case group "F"). By finding the intersection of desired depth (25 meters in the example, so we pick the next higher number) and new pressure group one can find the maximum bottom time at that depth (bottom row) and the residual nitrogen time (top row). In our example the maximum bottom time is 13 min and the residual nitrogen time is 12 min.
By adding bottom time and residual nitrogen time, the total bottom time can be calculated and the first table can be used again to calculate the pressure group after the 2nd dive. In our case the total bottom time is 25 min which lead to pressure group 'Q' after the second dive to 25 meters.
![table3: maximum bottom time after surface intervall](/divingComputer/Visualizations/table3MaxBottomTimeEx.png)

## Example and Result
The following images shows a diving profile of a repetitive dive. On the first dive the diver reaches a depth of 30 m and stays there for 17 min; resulting in pressure group 'L' (PG1 = L). She stays at the surface for 42 min which reduces her pressure group to 'F' (PG2 = F). On the second dive, the diver wants to dive to a depth of 25 m. The maximum time she can spend at this depth is 13 min which will result in pressure group 'Q' (PG3 = Q).
![Alt text](/divingComputer/Visualizations/divingProfile.png)

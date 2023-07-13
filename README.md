
# Demonstrator projects of Jennifer Weber
- The folder [Simulation](https://github.com/jennyweb/Demonstratoren/tree/main/Simulation) contains an example of a physical simulation in which heat transfer phenomena are modelled. This example describes are stone heating up while sitting in a fire. 

![Evolution of temperature over time](Simulation/ReadMeVisualization/result-temperature.gif)

- The folder [chemicalReaction](https://github.com/jennyweb/Demonstratoren/tree/main/chemicalReaction) shows an example of a chemical reaction. The following polymerization reaction is taken into account:
 
```math
\begin{align}
\text{M} + \text{M} &\rightarrow \text{P}_2 & \frac {\text{d}[P_2]} {\text{d}t} &= r\, [M][M] \\
\text{M} + \text{P}_2 &\rightarrow \text{P}_3 & \frac {\text{d}[P_3]} {\text{d}t} &= r \,[M][P_2] \\
& \vdots &  & \vdots \\
\text{M} + \text{P}_i & \rightarrow \text{P}_{i+1} & \frac {\text{d}[P_{i+1}]} {\text{d}t} &= r\, [M][P_{i}]
\end{align}
```
The resulting video shows the change of concentration of the polymers (with different chain length $i$) over time.
![Video of the progress of polymerization over time](chemicalReaction/progress-polymerization-over-time.gif)


- The folder [workWithGivenData](https://github.com/jennyweb/Demonstratoren/tree/main/workingWithGivenData) shows an example of how to read in data from a file and perform basic mathematical operations such as computing integrals. The resulting image shows the computed integral next to the analytical solution proving the correctness of my script. 
![Comparison of computed integral with the analytical solution](workingWithGivenData/calc-distanceVSgiven-distance.png)

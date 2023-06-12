# Model for a polymerization reaction

## Motivation

## Model of chemical reaction
It is assumed that the reaction mixture is homogeneously mixed at all times. The resulting polymers only react with the monomer
Therefore chemical reactions taking place can be described through the following equations on the left hand side. The change in concentration for the formed polymer in a given time intervall is given by the differential equation on the right hand side, where [$M$] is the concentration of the Monomer and [$P_i$] is the concentration of the polymer with chain length $i$. $r$ is the constant for reaction rate.

```math
\begin{align}
\text{M} + \text{M} &\rightarrow \text{P}_2 & \frac {\text{d}[P_2]} {\text{d}t} &= r\, [M][M] \\
\text{M} + \text{P}_2 &\rightarrow \text{P}_3 & \frac {\text{d}[P_3]} {\text{d}t} &= r \,[M][P_2]
\end{align}
```
```math
\text{M} + \text{P}_3 &rightarrow \text{P}_4 & \frac {\text{d}[P_4]} {\text{d}t} &= r\, [M][P_3]
\text{M} + \text{P}_i &rightarrow \text{P}_{i+1} & \frac {\text{d}[P_i]} {\text{d}t} &= r\, [M][P_{i-1}]
```
The differential equations can be solved as follows:
$$
\frac {\text{d}[P_2]} {\text{d}t} = r\, [M][M] \quad --> \quad \Delta [P_2] \, \Delta t = r [M][M]  
$$
Which can be rearranged to:
$$
\Delta [P_2] = r\, [M][M]\,\Delta t
$$
The concentration change for one time increment is given by:
$$
[P_2] (t+1) = [P_2](t)\, + \, r\, [M][M]\,\Delta t
$$
Analogous for chainlength = i
$$
[P_i] (t+1) = [P_i](t)\, + \, r\, [M][P_{i-1}]\,\Delta t
$$
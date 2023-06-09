# Model for a polymerization reaction

## Motivation

In this example I consider the case of a polymerization reaction taking place in a perfectly mixed batch reactor. 

![Icon of a batch reactor](ReadMeObjects/IconReactor.png)

## Model of the chemical reaction
The polymers only react with the monomer. Therefore, the chemical reactions are described by the following set of chemical equations

```math
\begin{align}
\text{M} + \text{M} &\rightarrow \text{P}_2 & \frac {\text{d}[P_2]} {\text{d}t} &= r\, [M][M] \\
\text{M} + \text{P}_2 &\rightarrow \text{P}_3 & \frac {\text{d}[P_3]} {\text{d}t} &= r \,[M][P_2] \\
\text{M} + \text{P}_3 &\rightarrow \text{P}_4 & \frac {\text{d}[P_4]} {\text{d}t} &= r\, [M][P_3] \\
& \vdots &  & \vdots \\
\text{M} + \text{P}_i & \rightarrow \text{P}_{i+1} & \frac {\text{d}[P_{i+1}]} {\text{d}t} &= r\, [M][P_{i}]
\end{align}
```


where $r = 0.01 \frac{L}{mol~s}$ is the reaction rate, $[M]$ is the monomer concentration and $[P_i]$ is the concentration of the polymer of chain length $i$. 

```math
\begin{align}
\text{M} + \text{P}_3 & \rightarrow \text{P}_4 & \frac {\text{d}[P_4]} {\text{d}t} &= r\, [M][P_3]\\
\text{M} + \text{P}_i & \rightarrow \text{P}_{i+1} & \frac {\text{d}[P_{i+1}]} {\text{d}t} &= r\, [M][P_{i}]
\end{align}
```

Numerically, the differential equation, of the dimer for example, is solved as
```math
\frac {\text{d}[P_2]} {\text{d}t} = r\, [M][M] \quad \approx \quad \frac {\Delta [P_2]}{\Delta t} = r [M][M]  \quad \leftrightarrow \quad \Delta [P_2] = r\, [M][M]\,\Delta t
```

with $\Delta t = 0.01$ s. The concentration change for one time increment is given by:
```math
[P_2] (t+1) = [P_2](t)\, + \, r\, [M][M]\,\Delta t
```
For an arbitrary chain length $i$, I apply
```math
[P_i] (t+1) = [P_i](t)\, + \, r\, [M][P_{i-1}]\,\Delta t
```
# Result
The following video shows the cjange of concentration of die different polymers over time.
![Alt text](progress-polymerization-over-time.gif)
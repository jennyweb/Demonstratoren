# Model for a polymerization reaction

## Motivation

## Model of chemical reaction

The chemical reactions taking place in the reaction mixture can be described as follows:

M + M -> P$_2$      chainlength = 2

M + P$_2$ -> P$_3$ chainlength = 3

M + P$_3$ -> P$_4$ chainlength = 4

M + P$_i$ -> P$_i$$_+$$_1$ chainlength = i

$$
\frac {\text{d}[P_2]} {\text{d}t} = r\, [M][M]
$$
$$
\frac {\text{d}[P_3]} {\text{d}t} = r \,[M][P_2]
$$
$$
\frac {\text{d}[P_4]} {\text{d}t} = r\, [M][P_3]
$$
$$
\frac {\text{d}[P_i]} {\text{d}t} = r\, [M][P_{i-1}]
$$

the differential equations can be solved as follows
$$
\frac {\text{d}[P_2]} {\text{d}t} = r\, [M][M] \quad --> \quad \Delta [P_2] \, \Delta t = r [M][M]  
$$
which can be resolved to:
$$
\Delta [P_2] = r\, [M][M]\,\Delta t
$$
The concentration change for one time increment is given by:
$$
[P_2] (t+1) = [P_2](t)\, + \, r\, [M][M]\,\Delta t
$$
analogous for chainlength = i
$$
[P_i] (t+1) = [P_i](t)\, + \, r\, [M][P_{i-1}]\,\Delta t
$$
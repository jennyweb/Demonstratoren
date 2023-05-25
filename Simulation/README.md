# Physical model for a stone in a campfire


This example is a demonstrator and hence focuses on the implementation and makes educated guesses for the physical variables where necessary. 

## Discretization

We apply a mesh spacing $\Delta x = 0.005 m$

## Underlying physical model

The underlying model is based on an energy balance, i.e. the enthalpy. Enthalpy is strongly related to temperature via the heat capacity $c_p$ and the mass $m$. 
$$
H = c_p m T
$$


We apply the following constants

| Variable                          | Symbol           | Value                   |Unit                      |  Comment              |
| :---                              |    :----:        |          ---:           |          ---:            |  ---:                 |
| Boltzmann constant                | $\sigma$         | 5.670 373 (21)×10−8     | $\frac{W}{m^2 K^4}$      | physical constant     |
| emissivity factor                 | $\epsilon$       | 0.3                     | -                        | educated guess        |
| 1-dimensional surface size        | $A$              | 0.005                   | $m$                      | is  mesh spacing $\Delta x$                      |
| ambient surrounding temperature   | $T_a$            | 278                     | $K$                      | educated guess                      |
| surrounding air temperature       | $T_\text{air}$   | 278                     | $K$                      | educated guess                      |
| heat transfer coefficient         | $h$              | x                       | $\frac{W}{m^2 K}$        |                       |




Enthalpie change is given by

$$
\frac{\text{d}H}{\text{d}\text{t}} = \dot{H} \Delta t
$$

where 

$$
\dot{H}  = \dot{H}_\text{radiation} + \dot{H}_\text{convection} + \dot{H}_\text{conduction} + \dot{H}_\text{source}
$$

Each of the elements is described in the following

1. First, change in enthalpy at the stone boundary due to radiation $\dot{H}_\text{radiation}$  is given 

$$
\dot{H}_\text{radiation} = \epsilon \sigma A (T^4 - T_a^4)
$$

2. Heat transport at the stone boundary due to convection is given by 

$$
\dot{H}_\text{convection} = h A (T - T_\text{air})
$$


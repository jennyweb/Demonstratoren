
# Data Fitting 

## Motivation
The goal of this project is to fit a given equation to given data. This has been performed by two means. First, the Nelder-Mead algorithm has been implemented and applied. Second, a third-party library (i.e. Scipy) has been used as this library contains the very same nelder-mead algorithm so that the results can be compared to validate the functionality of the own algorithm. 

## Theory

The underlying data set that has been used for this set is a particle size distribution as commonly measured in powder problems. Usually, such a particle size distribution follows a lognormal distribution. Such a lognormal distribution has the following shape: Given a normal distribution with mean $\mu$ and standard deviation $\sigma$, then a variable $x$ has a log-normal distribution if $\log(x)$ is normally distributed. The probability density function for the log-normal distribution is then given by 

$$
p(x) = \frac{1}{\sigma \, x \, \sqrt{2 \pi}} e^{\left(-\frac{(\ln(x)-\mu)^2}{2 \, \sigma ^2}\right)}
$$



Then the deviation is calculated. The two different fit- methods decrease the deviation and find the correct values for sigma and µ.
The Nedler Mead method was implemented by myself and for comparison the SciPy function optimize.minimize() was used with method = 'Nelder Mead'.
For the implementation the class vector was created. An initial guess for sigma and µ was made and three initial vectors were created to form the simplex. The errors of the vectors u, v, w increases in the following oder:

u < v < w

W is refleced at the midpoint between u and v. Is the error of the reflected w smaller than of v but bigger than u, it is made the new v and the old v becomes w.
Is the error smaller than both u and v than the point is extended further. Now the errors of the further extended point and the reflected w are compared. The point with the smaller error will be made the new u. U will become v and v will become w.
If the reflected w doesn't outperform v or u, the 1/4 and 3/4 distance between w and the reflected w will be tested, the best is chosen. Otherwise the simplex is shrinked. The new v will be the midpoint between u and v, analogous for w.

## Result 
After 60 iterations of the self-implemented algorithm resulted in the same value for sigma and µ as the Scipy function. The video shows the evolution of the self-implemented algorithm over time.

Solution scipy: µ = 3.754e+00 sigma = 2.918e-01

Own algorithm : µ = 3.754e+00 sigma = 2.918e-01

![Alt text](VisualizationOfFittingProgress.gif)

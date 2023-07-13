
# Data Fitting 
# Motivation
The goal of this project is to fit a given dataset using the SciPy library and impementing the fit myself. Both fits result in the same values for the variables.

# Theory

Given a normal distribution with mean $\mu$ and standard deviation $\sigma$. Here, a variable $x$ has a log-normal distribution if $\log(x)$ is normally distributed. The probability density function for the log-normal distribution is

$$
p(x) = \frac{1}{\sigma x \sqrt{2 \pi}} e^{\left(-\frac{(\ln(x)-\mu)^2}{2 \sigma ^2}\right)}
$$

 Hence, in order to compute a lognormal distribution, I first compute the logarithmic mean
$$
\bar{x}_\text{log} = \ln(\mu) - 0.5 \, \sigma ^2
$$

and then use the numpy module to create lognormal distributions

Then the deviation is calculated. The two different fit- methods decrease the deviation and find the correct values for sigma and µ.
The Nedler Mead method was implemented by myself and for comparison the SciPy function optimize.minimize() was used with method = 'Nelder Mead'.
For the implementation the class vector was created. An initial guess for sigma and µ was made and three initial vectors were created to form the simplex. The errors of the vectors u, v, w increases in the following oder:
u < v < w
W is refleced at the midpoint between u and v. Is the error of the reflected w smaller than of v but bigger than u, it is made the new v and the old v becomes w.
Is the error smaller than both u and v than the point is extended further. Now the errors of the further extended point and the reflected w are compared. The point with the smaller error will be made the new u. U will become v and v will become w.
If the reflected w doesn't outperform v or u, the 1/4 and 3/4 distance between w and the reflected w will be tested, the best is chosen. Otherwise the simplex is shrinked. The new v will be the midpoint between u and v, analogous for w.

# Result 

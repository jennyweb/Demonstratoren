
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

The I calculate the deviation and use the SciPy function optimize.minimize to decrease the deviation and find the correct values for sigman and µ (here the Nelder Mead method of that function is used).

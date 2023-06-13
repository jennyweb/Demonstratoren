

Given a normal distribution with mean $\mu$ and standard deviation $\sigma$. Here, a variable $x$ has a log-normal distribution if $\log(x)$ is normally distributed. The probability density function for the log-normal distribution is

$$
p(x) = \frac{1}{\sigma x \sqrt{2 \pi}} e^{\left(-\frac{(\ln(x)-\mu)^2}{2 \sigma ^2}\right)}
$$

<!-- Hence, in order to compute a lognormal distribution, we first compute the logarithmic mean
$$
\bar{x}_\text{log} = \ln(\mu) - 0.5 \, \sigma ^2
$$

and then use the numpy module to create lognormal distributions

 -->

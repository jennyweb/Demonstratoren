## Reading data and data integration
# Motivation
This project works as a demonstration of my skills to work with data provided by a text file.
# Setup
The data file contains one column for time, velocity and distance. The distance column is later used to verify the calculated result.
The steps executed in the script are the following:
- reading data using pandas and csv.DictReader
- calculating the time intervall d$t$ and the covered distance during d$t$
- adding up to covered distance up to a given time
- plotting the calculated data using matplotlib and comparing it to the reference data
# Calculations

The time intervall d$t$ was calculated by subtracting $t_i$  by $t_{i-1}$.
The distance that was covered in a time intervall d$t$ was calculated as follows:
$$
\text{distance}(t) = \text{velocity}(t) * \text{d}t
$$
In order to calculate the complete distance covered up to a time $t$ the sum was formed.
$$
distance = \sum \text{velocity}(t) * \text{d}t
$$

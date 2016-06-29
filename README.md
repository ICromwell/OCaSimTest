# OCaSimTest
A test of the basic functionality of an individual sampling model of oral cancer treatment
#

An individual sampling model is a subset of a discrete event simulation model (see http://www.ncbi.nlm.nih.gov/pubmed/15099459
for more explanation) wherein individual entities are created and move through a simulated environment according to the underlying
probabilities of each move. Each move occurs within simulated time - this is known as a 'time to event' process.

The model in this directory is my first attempt to create such a model in Python. It uses the package Simpy to run the
time-to-event processes, and ordinary Python functions for everything else (see https://simpy.readthedocs.io/en/latest/). This
code will be used to create a larger Whole Disease Model of oral cancer for my graduate thesis.

Thanks go to Stavros Korokithakis of Stochastic Technologies (http://www.stochastic.io/) for his instrumental and ongoing guidance,
and to Peter Grayson in the Simpy Google group for helping figure out some of the key syntax.

If you use this code, I would ask that you please notify me (icromwell@bccrc.ca), as I am curious to see what other peoples'
experiences are, and where there are areas for improvement.

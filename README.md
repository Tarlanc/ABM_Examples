# ABM_Examples
In this repository, some examples of Agent Based Models are shared. The models are written in R and Python and may be used to study the feasibility and intricacies of ABMs.

## Covid-Sim.R
This simulation uses a network graph to simulate the contagion of a contagious agent (inspired by Sars-CoV2) through a small network with one initially infected agent.

## Chase.py
This is a python script that may be used as a module for generating colorful simulations with turtles.
The script contains classes for the environment and agents that may be used to build quick and easy simulations.
In the script, there are three example simulations that may be done in this framework. Each one of these may be extended, refined, and altered to suit specific needs. Or just use it for fun to see whether the zombie apocalypse is really the end.

## evolution.py
This is a python script that may be used as a module for optimizing a multi-parameter problem with a genetic algorithm. It contans just one class named `GeneticAlgorithm` and a simple model with a non-linear problem to demonstrate its use.
An object of the class `GeneticAlgorithm` is capable of adapting to the outputs of a specific function passed to it and will try to reach the highest possible result.
When a solution is reached (either due to time restriction or reaching convergence), the results and optimization history may be exported to a csv for further analysis.

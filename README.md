# ABM_Examples
In this repository, some examples of Agent Based Models are shared. The models are written in R and Python and may be used to study the feasibility and intricacies of ABMs.

## Covid-Sim.R
This simulation uses a network graph to simulate the contagion of a contagious agent (inspired by Sars-CoV2) through a small network with one initially infected agent.

## easyabm.py
This is a python script that may be used as a module for generating colorful simulations with turtles.
The script contains classes for the environment and agents that may be used to build quick and easy simulations.
In the script, there are three kinds of example simulations that may be done in this framework (Balls, Predators, Boids). Each one of these may be extended, refined, and altered to suit specific needs.
The different classes demonstrate how to add methods and teach the agents new behavior.

## evolution.py
This is a python script that may be used as a module for optimizing a multi-parameter problem with a genetic algorithm. It contans just one class named `GeneticAlgorithm` and a simple model with a non-linear problem to demonstrate its use.
An object of the class `GeneticAlgorithm` is capable of adapting to the outputs of a specific function passed to it and will try to reach the highest possible result.
When a solution is reached (either due to time restriction or reaching convergence), the results and optimization history may be exported to a csv for further analysis.

## networksim.R
This is an R-Script that simulates the contagion in randomly generated networks, using two attributes: Knowing information and being willing to share information.
The script generates an animated GIF that shows the progress of contagion for networks with differing density.

## Conformity.R
This is an R-Script that simulates an attenuation process in a grid. Each agent in the grid has an attitude and a talking propensity.
According to the spiral of silence, agents talk if they are in line with their environment and are silent if they are not.
The environment of each agent is only observable through talking agents, leading to an increase of minute initial biases.

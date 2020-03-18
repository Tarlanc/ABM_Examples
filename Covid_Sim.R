# Contagion simulation
# Required packages are igraph and (if you want
# to animate the results in a GIF) animate

library(igraph)
library(animation)


## Let's assume the situation of a small community
## of about 100 (or any number) of households.

## First, we create an adjacency matrix of N households

## The connections between the households are defined
## in the adjacency matrix. The higher the value
## the stronger the contact between households,
## be it through handshakes, children going to the
## same school or mutually shared shopping carts.
## The adjacency matrix has a diagonal of 0
## and is symmetric for the purpose of an easy model.

houses = 100
adjmat = matrix(runif(houses**2,-1,4),nrow=houses)
diag(adjmat)=0
adjmat[lower.tri(adjmat)] = t(adjmat)[lower.tri(adjmat)]

## Social Distancing: Reduce the value of the adjacency
## matrix. If a value dropps below 0, the nodes
## will not be connected anymore.

adjmat=adjmat-1

## Wash hands: Reduce the transmission vectors by
## lowering the intensity of contact.
adjmat=adjmat/1.5

## Remove transmission paths below 0
adjmat[adjmat<0]=0

## Each household has a different level of contagiousness
## This may be due to the number of people in the house
## or by the severity of symptoms of inhabitants.
nodes = rnorm(houses,3,.5)


## Create a network graph from this matrix
g = graph_from_adjacency_matrix(adjmat, 
                                mode="undirected", 
                                weighted = TRUE)

g = set_vertex_attr(g, "Cont", value=nodes) # Add the contagiousness as node attribute
g = set_vertex_attr(g, "State", value=1)    # Everyone is sane (1) at the moment
pzero = as.integer(runif(1,1,houses)) ## Define a random patient zero
V(g)$State[pzero]=2 ## Change the state of patient zero to 2 = sick
V(g)$CDate=NA ## Contraction Date
V(g)$CDate[pzero]=0 ## Set the contraction Date of patient zero to 0

## Network cosmetics: Change edge and Vertex attributes
## for plotting
E(g)$width = E(g)$weight*2-1 ## Make edges with high transmission probability wider
E(g)$color = "#808080"
V(g)$color = c("#aaaaaa","#ff0000","#00ff00")[V(g)$State] ## Paint infected nodes red and recovered ones green
V(g)$vertex.size = V(g)$Cont 

# print(vertex.attributes(g))

l = layout.kamada.kawai(g) ## Compute a sensible layout for all future plots

plot(g,layout=l) ## Plot with this layout once, just to see the initial state.


ani.record(reset = TRUE) ## If an animation is to be done: Start the recording
oopts = ani.options(interval = .2) ## Set the animation parameter to 0.2 seconds per image

par(mfrow=c(1,2)) ## Graphics parameter: Two adjacent plots

## Initiate four recording vectors:
## spread: number of people that have contracted the virus
## inf: number of currently infected people
## rec: number of currently recovered people
## date: Current day since day zero (infection of patient zero)
v.spread = c(1/houses)
v.inf = c(1/houses)
v.rec = c(0)
v.date = c(0)


## Start the simulation by setting the first day to 0
## The simulation will run until two months have passed
## or until no one is sick anymore.
## Whatever comes first.

day = 0
while(day < 60 & v.inf[length(v.inf)]>0){
  day = day +1 ## Progress 1 day

  ## Compute infection vector:
  ## For each household, compute the infection
  ## risk, based on the transmission vectors and
  ## the contagiousness of all infectious households.
  V(g)$Sick = V(g)$State==2 & day>(V(g)$CDate+2) & day<(V(g)$CDate+7)
  V(g)$Recovered = V(g)$State==3
  ivec = colSums(V(g)$Sick * adjmat)*V(g)$Cont
  
  ## Compute the luck vector:
  ## Each household gets to roll the dice for luck.
  ## If luck is higher than the current infection risk,
  ## the household will not be infected.
  luck = runif(houses,1,300)
  
  V(g)$CDate[ivec>luck & V(g)$State==1]=day ## Set infection date of newly infected
  V(g)$State[ivec>luck & V(g)$State==1]=2 ## Set all newly infected to State=2 (sick)
  V(g)$State[day>(V(g)$CDate+14)]=3 ## Recovering after 2 weeks
  
  ## Update plot
  V(g)$color = c("#aaaaaa","#ff0000","#00ff00")[V(g)$State] ## Update colors
  plot(g,layout=l)
  #print(vertex.attributes(g))
  
  
  ## Update all recording vectors
  v.spread = c(v.spread,mean(V(g)$State>1))
  v.inf = c(v.inf,mean(V(g)$State==2))
  v.rec = c(v.rec,mean(V(g)$State==3))
  v.date = c(v.date,day)
  
  ## Use the recording vectors to plot the line plot
  plot(v.date,v.spread,type="l",ylim=c(0,1),
       xlab="Day since first infection",
       ylab="Share of households")
  lines(v.date,v.inf,col="red")
  lines(v.date,v.rec,col="green")
  ani.record() ## Add current plot to animated GIF
}

## Export the recorded images as animated GIF to the
## current working directory.

saveGIF(ani.replay(),
        movie.name="Example.gif",
        ani.width=800,ani.height=400)


## Simple network contagion simulation.
## Random networks are generated to measure contagion speed and efficiency

## Library igraph is required for the simulation.
library(igraph)

## Library animation is optional. 
## It is used to generate an animated GIF from the results.
library(animation)

set.seed(2020)

ani.record(reset = TRUE) ## Used for animation

for(rlimit in c(.8,1.0,1.3,1.5,1.7,1.9,2.1)){
  ## rlimit is a z-Value used for generating links
  ## rlimit = 1.96 would lead to a 5% dense model
  
  nnodes = 100  ## Number of nodes in each network
  adjmat = matrix(0,nrow=nnodes,ncol=nnodes)  ## Generate Empty adjacency matrix
  adjmat[rnorm(nnodes**2,0,1)>rlimit]=1       ## Add random edges
  colnames(adjmat)=rownames(adjmat)=c(1:nnodes) ## Label the nodes
  
  ## From the random adjacency matrix, adirected graph is built
  
  g = graph_from_adjacency_matrix(adjmat, 
                                  mode="directed", 
                                  weighted = TRUE)
  
  ## Cosmetics
  ## Colors and arrow width
  
  E(g)$arrow.size=.2
  E(g)$curved = .2
  E(g)$width = E(g)$weight*2-1
  E(g)$color = "#808080"
  
  V(g)$color = c("#aaaaaa")
  V(g)$label.cex=.5
  V(g)$label.color="black"
  V(g)$size=10
  
  l = layout.kamada.kawai(g) ## Define a clean layout for all following graphs.
  
  plot(g,layout=l)
  
  V(g)$Wissen = 0  ## Knowledge of each node (all set to 0)
  V(g)$Teilen = 0  ## Sharing propensity of each node (all set to 0)
  
  initiator = sample(V(g)$name,1)  ## Randomly choose one initial seed
  V(g)$Teilen[as.integer(initiator)]=1  ## The initial seed shares the information
  
  anz.wissende = 1  ## Number of nodes that know
  anz.teilende = 1  ## Number of nodes that share
  step = 0          ## Current time
  
  ## Vectors for subsequent data visualization
  
  v.step = c(0)     ## Vector of times
  v.wiss = c(1)     ## Vector of knowing
  v.teil = c(1)     ## Vector of sharing
  
  par(mfrow=c(1,2))  ## Initiate the graphics parameter to show two plots
  
  V(g)$color[V(g)$Wissen>0]=c("#8080ff")  ## Knowing nodes are colored blue
  V(g)$color[V(g)$Teilen==1]=c("#ff0000") ## Knowing nodes are colored red
  plot(g,layout=l)
  plot(0,0,pch="",xlim=c(0,20),ylim=c(0,1),xlab="Time",ylab="Degree",
       main=paste("Inhibition:",rlimit))
  ani.record()  ## Used for animation
  
  
  ### Actual Simulation starts here.
  ### ------------------------------
  ###
  ## While not the whole network is infected/knowing, continue the simulation.
  ## In each step, for each node, compute the knowledge based on knowing
  ##   nodes among direct neighbors.
  ## Set random thresholds for each node on how intense the knowledge has to
  ##   be to share the information.
  ## Adjust the colors of the plot and the record of knowing/sharing nodes
  ## Plot and store the information.
  
  while(anz.wissende < nnodes & step<20){
    step=step+1
    for(v.num in 1:nnodes){
      shares = V(g)$Teilen[adjmat[,v.num]>0]
      strengths = adjmat[,v.num][adjmat[,v.num]>0]
      impact = sum(shares*strengths)
      V(g)$Wissen[v.num]=impact
    }
    
    grenze = runif(nnodes,0.5,3) ## Random threshold for sharing
    V(g)$Teilen[V(g)$Wissen>grenze]=1 ## All nodes with knowledge that exceeds the threshold, then share.
    
    V(g)$color[V(g)$Wissen>0]=c("#8080ff")
    V(g)$color[V(g)$Teilen==1]=c("#ff0000")
    
    anz.wissende = sum(V(g)$Wissen>0)
    anz.teilende = sum(V(g)$Teilen==1)
    v.step = c(v.step,step)
    v.wiss = c(v.wiss,anz.wissende)
    v.teil = c(v.teil,anz.teilende)
    
    plot(g,layout=l)
    plot(v.step,v.wiss/nnodes,type="l",xlim=c(0,20),ylim=c(0,1),xlab="Time",ylab="Degree",
         col="#8080ff",main=paste("Inhibition:",rlimit))
    lines(v.step,v.teil/nnodes,col="red")
    ani.record()  ## Used for animation: Record the current plot.
  }
}

## Store the animation as GIF:

oopts = ani.options(interval = .4)  ## Set time step to 0.4 seconds
ani.replay()                        ## Display animation in Plot

## Store as GIF with specified width and height:
saveGIF(ani.replay(),movie.name="Example.gif",ani.width=800,ani.height=400)


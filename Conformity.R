
## Simulation of polarization in a heterogeneous society
## Simulations of this kind may be used to simulate opinion dynamics.

library(animation) ## Used to create an animated GIF

## Each agent is a point on a cartesian X-Y-grid.
## Each agent has an attitude that is drawn from N(3,1)
## Each agent has a propensity to talk which is initially 1 (active)


## Function that allows the generation of RGB codes based on a value between 1 and 5

Einst.Farbe = function(Einstellung){
  ## Transform value between 1 and 5 to a value between -1 and 1:
  x = (Einstellung-3)/2
  if(x<=-1){x=-1}
  if(x>=1){x=1}
  
  maincol = abs(x)*.4+.6 ## Red or green
  offcol = (1-abs(x))*.6  ## other colors
  
  if(x>=0){col = rgb(offcol,maincol,offcol)}
  if(x<0){col = rgb(maincol,offcol,offcol)}
  return(col)
}

Einst.Farbe(5) ## Should be green
Einst.Farbe(1) ## Should be red
Einst.Farbe(3.7) ## Should be greenish


###  Actual simulation

set.seed(2021) ## Set seed for reproducability

## Each agent is a point on a cartesian X-Y-grid.
## Each agent has an attitude that is drawn from N(3,1)
## Each agent has a propensity to talk which is initially 1 (active)

x = c()
y = c()
for(xi in 1:15){
  for(yi in 1:15){
    x = c(x,xi)
    y = c(y,yi)
  }
}

n.agents = length(x)
agents = as.data.frame(cbind(x,y))
agents$Einstellung = rnorm(n.agents,3.0,1)  ## Compute attitude of each agent
agents$Reden = 1 ## All agents speak

recording = data.frame("Step"=0,
                       "Mean_Att"=mean(agents$Einstellung),
                       "Mean_Att_Expressed"=mean(agents$Einstellung[agents$Reden==1]),
                       "Share_Express"=mean(agents$Reden))

ani.record(reset = TRUE) ## Reset recording
par(mfrow=c(1,2))

nsteps = 30
for(schritt in 1:nsteps){
  for(a in 1:n.agents){
    xpos = agents$x[a]
    ypos = agents$y[a]
    distanzen = (agents$x-xpos)**2+(agents$y-ypos)**2
    umgebung = (1:n.agents)[distanzen<5&distanzen>0]  ## Define the environment for this agent
    u.einst = agents$Einstellung[umgebung] ## Get attitudes in the environment
    u.reden = agents$Reden[umgebung]       ## Check whether the agents in the environment are talking
    u.klima = mean(u.einst[u.reden==1])    ## Compute the mean attitude of talking neighbors
    dissonanz = abs(u.klima-agents$Einstellung[a])  ## Compute difference from own opinion (dissonance)
    if(is.na(dissonanz)){dissonanz=0}
    
    ## The agent should be silent if dissonance with environment is > 0.5
    ## Otherwise, the agent is speaking and gets more confident about the attitude
    agents$Reden[a]=1
    if(dissonanz>0.5){
     agents$Reden[a]=0
    } else {
      if(agents$Einstellung[a]>3 & agents$Einstellung[a]<5){
        agents$Einstellung[a]=agents$Einstellung[a]+.1
      } else if(agents$Einstellung[a]>1){
        agents$Einstellung[a]=agents$Einstellung[a]-.1
      }
    }
    
    
    ## The agent should completely change the opinion if dissonance exceeds 1.
    if(dissonanz>1){
       agents$Einstellung[a] = mean(c(agents$Einstellung[a],u.klima))
    }
  }
  
  ## Update the picure
  agents$Farbe = sapply(agents$Einstellung,Einst.Farbe)
  agents$Symbol = c(4,1)[agents$Reden+1]
  
  plot(agents$x,agents$y,pch=15,col=agents$Farbe,cex=3)
  points(agents$x,agents$y,pch=agents$Symbol,cex=2)
  #plot(density(agents$Einstellung))
  plot(recording$Step,recording$Mean_Att,xlim=c(0,nsteps),
       ylim=c(1,5),type="l",col="blue", main="Attitudes in population")
  lines(recording$Step,recording$Mean_Att_Expressed,col="black")
  legend("topleft",c("True","Expressed"),lwd=1,col=c("blue","black"))
  
  
  ani.record()

  recording = rbind(recording, data.frame("Step"=schritt,
                         "Mean_Att"=mean(agents$Einstellung),
                         "Mean_Att_Expressed"=mean(agents$Einstellung[agents$Reden==1]),
                         "Share_Express"=mean(agents$Reden)))
  
}


oopts = ani.options(interval = .5)
saveGIF(ani.replay(),movie.name="Example.gif",ani.width=700,ani.height=400)

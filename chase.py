import time
import math
import random

from tkinter import *
random.seed()

############################ About this script
#
# This script is an example for easy and quick Agent-Based Simulations in R, using a graphical display (or not).
# It contains several classes that may be used in simulations and some functions that illustrate how to use them.
#
# Classes:
# - Display: This class opens a simple tkinter canvas of a given witdth and height. Objects of this class may then be used to
#            display the progress of the simulation.
# - Agent: This class is a standard class for agents in the simulation. It contains methods to move the agents around
#          in the defined environment and there are some basic parameters for Agents in this class.
# - Ball: The Class 'Ball' is a child of Agent. It is a very simple agent with only one additional method: It can deflect from
#         planes.
# - Human: This class is also a child of Agent. It has some additional functions that allow the agents to decide on the next
#          step or may be used to kill the Agent or get the bearings to other coordinates.
#
# Functions:
# - rainbow: A simple color generator.
# - random_balls: A function to generate Agents of the class Ball, each with a different random color.
# - simulate_billiard: An example simulation of a very simplistic billiard game where the balls do not see each other
#                      but are deflected from the walls.
# - simulate_chase: An example of a simulation where green agents of class Human (prey) are hunted down and killed by
#                   red agents of class Human (hunter).
# - simulate_standoff: An example of a simulation with n agents of class Human, where each agent hunts the next in line
#                      and flees from the previous. Each agent has a suitor and a target and the simulation will either
#                      end in an endless circle or in wild eddies.
#


class Display(Frame):
    def __init__(self, master=None, width = 900, height=600):
        ## Initialize this class with a width and height to define the size of the canvas.
        Frame.__init__(self,master)
        top=self.winfo_toplevel() #Flexible Toplevel of the window
        top.rowconfigure(3, weight=1)
        top.columnconfigure(3, weight=1)
        self.grid(sticky=N+S+W+E)
        self.width = width
        self.height = height

        settings = {'Width':self.width,
                    'Height':self.height}

        self.coords = StringVar()
        self.coords.set("")

        self.ysc = Scrollbar(self,orient=VERTICAL)
        self.ysc.grid(row=3,column=2,sticky=N+S)
        self.xsc = Scrollbar(self,orient=HORIZONTAL)
        self.xsc.grid(row=2,column=3,sticky=W+E)

        self.feld = Canvas(self,bg="#ffffff",height=settings['Height'],
                           width=settings['Width'],
                           yscrollcommand=self.ysc.set,
                           xscrollcommand=self.xsc.set,
                           scrollregion=(0, 0, self.width, self.height))
        self.feld.grid(row=3,column=3,sticky=N+E+S+W)
        self.ysc['command']=self.feld.yview
        self.xsc['command']=self.feld.xview

        self.feld.bind("<Motion>",self.show_coord)
        self.feld.bind("<Leave>",self.hide_coord)

        self.cleg = Label(self,textvariable=self.coords)
        self.cleg.grid(row=0,column=3,sticky=W)
        self.xlin = Canvas(self,width=settings['Width'],height=20,bg="#eeeeff")
        self.xlin.grid(row=1,column=3,sticky=N,columnspan=3)
        self.ylin = Canvas(self,width=30,height=settings['Height'],bg="#eeeeff")
        self.ylin.grid(row=3,column=1,sticky=E)
        

        for tick in range(0,settings['Width'],50):
            a = self.xlin.create_line(tick,20,tick,15,fill="#000000")
        for tick in range(100,settings['Width'],100):
            a = self.xlin.create_line(tick,20,tick,11,fill="#000000")
            a = self.xlin.create_text(tick,8,text=str(tick))

        for tick in range(0,settings['Height'],50):
            a = self.ylin.create_line(30,tick,25,tick,fill="#000000")
        for tick in range(100,settings['Height'],100):
            a = self.ylin.create_line(30,tick,20,tick,fill="#000000")
            a = self.ylin.create_text(3,tick,anchor=W,text=str(tick))


    def show_coord(self,event=''):
        ## Method used when the mouse enters the canvas. In this case, the coordinates of the
        ## Pointer are indicated in the label self.cleg at the top of the window.
        x = event.x
        y = event.y
        #print(x,y)
        self.coords.set("X: "+str(x)+" / Y: "+str(y))

    def hide_coord(self,event=''):
        ## Method to remove the coordinate display if the mouse is outside the window.
        self.coords.set("")


class Agent():
    def __init__(self,master=None,x=None,y=None,direction=None,size=6,atype="Turtle"):
        ## Each agent has x and y coordinates, an initial direction (measured in radian angle), a size, and an optional type.
        ## The first argument (master) is the canvas on which the agent lives. If this argument is omitted,
        ## the canvas will be 1000x1000 units and the progress is not displayed. If master is a list of two integers,
        ## the canvas will have the measurements master[0] x master[1] and no graphic output is possible.
        ## If no x, y, or direction are passed, random values will be generated.

        if master==None:         ## Definition of the range of this agent.
            self.limit = (size,size,1000-size, 1000-size)
        elif type(master)==list:
            self.limit = (size,size,master[0]-size, master[1]-size)
        else:
            self.limit = (size,size,master.width-size, master.height-size)

        ## Current x position. Is updated during movement.
        if x==None:
            self.xpos = random.randint(self.limit[0],self.limit[2])
        else:
            self.xpos = x
            
        ## Current y position. Is updated during movement.
        if y==None:
            self.ypos = random.randint(self.limit[1],self.limit[3])
        else:
            self.ypos = y

        ## Corrent direction. Given in radian Degrees [0,2pi]
        if direction==None:
            self.direction = random.random()*2*math.pi
        else:
            self.direction = direction
        
        self.size = size         ## Size of the agent.
        self.master = master     ## Whatever was passed as master. Usually a Display object.
        self.type=atype          ## Type of the Agent
        self.speed = 1           ## Speed of the Agent in units per Tick
        self.delay=0.0           ## Delay in the motion of the agent. If the simulation runs too fast, just set it to a small value (e.g.: 0.01)

        self.col = "#aaaaaa"
        self.draw()

    def position(self):
        ## Method to determine the current position of all corners of the
        ## agent. This method is required to draw the shape where it needs to be.
        pos = [int(self.xpos),int(self.ypos)]
        pos.append(round(self.xpos+self.size*math.cos(self.direction)))
        pos.append(round(self.ypos+self.size*math.sin(self.direction)))
        return pos

    def draw(self):
        ## Initial drawing of the agent. After the agent is drawn for the first
        ## time, don't use this method again. Use .shift() to move existing agents.
        p = self.position()
        self.id = self.master.feld.create_oval(p[0]-self.size,
                                               p[1]-self.size,
                                               p[0]+self.size,
                                               p[1]+self.size,
                                               fill=self.col,
                                               outline="#000000",
                                               width=1)
        self.id2 = self.master.feld.create_oval(p[2],p[3],p[2],p[3],
                                                fill="#000000",
                                                outline="#000000",
                                                width=self.size/2)
        self.master.feld.update()

    def shift(self):
        ## Move the agent to the current xpos/ypos. This function updates the graphic display
        ## for this agent.
        try:
            h = self.master.height    
            p = self.position()
            self.master.feld.coords(self.id,[p[0]-self.size,
                                             p[1]-self.size,
                                             p[0]+self.size,
                                             p[1]+self.size])
            self.master.feld.coords(self.id2,[p[2],p[3],p[2],p[3]])
            self.master.feld.itemconfigure(self.id,fill=self.col)
            self.master.feld.update()
        except:
            pass ## No active arena

    def move(self,step=None):
        ## Compute the next xpos and ypos, depending on the current position, speed, and direction.
        ## At the end, the .shift() method is called to actually move the representation.
        ## If a number of steps is defined, the movement will be divided to this number of steps.
        if type(step)==int:
            step = 5
            steps = int(self.speed/step)
            if steps<1:steps=1
            step = self.speed/steps
        else:
            step=self.speed
            steps=1

        for t in range(steps):
            self.xpos+=step*math.cos(self.direction)
            self.ypos+=step*math.sin(self.direction)
            if self.xpos<self.limit[0]:
                self.xpos=self.limit[0]
                self.direction+=.1
            elif self.xpos>self.limit[2]:
                self.xpos=self.limit[2]
                self.direction+=.1
            if self.ypos<self.limit[1]:
                self.ypos=self.limit[1]
                self.direction+=.1
            elif self.ypos>self.limit[3]:
                self.ypos=self.limit[3]
                self.direction+=.1
            self.shift()
            time.sleep(self.delay)

class Ball(Agent):
    ## Child of the class Agent that adds one method.
    def boing(self,phi):
        ## Elastic reflection on a collision surface with angle phi
        self.direction = 2*(phi-self.direction)+self.direction       
        if self.direction>2*math.pi:
            self.direction-=2*math.pi
        elif self.direction<0:
            self.direction+=2*math.pi


class Human(Agent):
    ## Child of the class Agent that adds some methods.
    def relpos(self,coords):
        ## Determine the distance and relative position of a set of target coordinates.
        xd = coords[0]-self.xpos
        yd = coords[1]-self.ypos
        d = (xd**2+yd**2)**.5
        if d < 1: d = 1 ## Distance of 0 should be impossible
        return (d,xd,yd)

    def kill(self):
        ## Change the color, speed, and type of an agent to kill it off.
        ## The direction of this agent may still change and be updated if you
        ## go on forcing the corpse to make decisions.
        self.speed=0
        self.col="#ffffff"
        self.type="Corpse"
        self.shift()

    def gotcha(self,alist,t="Hunter"):
        ## Check, whethe the agent is touched by another Human agent of a given type.
        ## The method returns True if there is contact.
        g = False
        for a in alist:
            if a.type==t:
                d = ((self.xpos-a.xpos)**2+(self.ypos-a.ypos)**2)**.5
                if d < self.size+a.size:
                    g = True
        return g

    def decide(self, flee=[], chase=[]):
        ## Method to determine the next step of an agent and change the direction accordingly.
        ## The method takes two lists of Human agents. The first list contains the agents from
        ## which this agent tries to flee. The second list contains the agents it wants to chase.
        ## The new direction will be chosen to avoid the members of flee and get closer to the
        ## members of chase. Each member is weighted by their distance to this agent.


        ## Compose a list of coordinates and their distances
        ## from which the agent is fleeing.

        flist = []
        for p in flee:
            flist.append(self.relpos((p.xpos,p.ypos)))
        outer = 50
        inner = 10

        ## The walls are also entities from which an agent flees.
        ## If the agent reaches the 'outer' threshold next to a wall, it is repulsed
        ## by this threshold.
        ## If the agent breaches the threshold (because they also flee other agents),
        ## it is repulsed by its own image next to them on the wall.
        
        if self.xpos < self.limit[0]+inner:
            flist.append(self.relpos((self.xpos-2,self.ypos)))
        elif self.xpos > self.limit[2]-inner:
            flist.append(self.relpos((self.xpos+2,self.ypos)))
        elif self.xpos < self.limit[0]+outer: ## Flee from the wall as well
            flist.append(self.relpos((self.limit[0],self.ypos)))
        elif self.xpos > self.limit[2]-outer:
            flist.append(self.relpos((self.limit[2],self.ypos)))

        if self.ypos < self.limit[1]+inner:
            flist.append(self.relpos((self.xpos,self.ypos-2)))
        elif self.ypos > self.limit[3]-inner:
            flist.append(self.relpos((self.xpos,self.ypos+2)))
        elif self.ypos < self.limit[1]+outer:
            flist.append(self.relpos((self.xpos,self.limit[1])))
        elif self.ypos > self.limit[3]-outer:
            flist.append(self.relpos((self.xpos,self.limit[3])))

        ## Compose the list of targets.

        slist = []
        for p in chase:
            slist.append(self.relpos((p.xpos,p.ypos)))


        ## Compute the maximal distance to any enemy or friend (for weighting purposes)

        md = self.limit[2]**2
        for e in flist+slist:
            if e[0]<md:md=e[0]

        ## Compute the mean desired position, away from entities it wants to flee and close
        ## to entities, it wants to catch.

        tx = 0.0
        ty = 0.0
        np = 0.0

        for e in flist:
            tx-=e[1]*(md/e[0]**2)
            ty-=e[2]*(md/e[0]**2)
            np+=(md/e[0])
        for e in slist:
            tx+=e[1]*(md/e[0]**2)
            ty+=e[2]*(md/e[0]**2)
            np+=(md/e[0])

        if np>0:
            tx = tx/np
            ty = ty/np

            td = (tx**2+ty**2)**.5
            target = (tx/td,ty/td)
        else:
            target=(0,0)

        ## The desired direction is a normalized vector.


        ## Try different angles and pick the one that lets the agent
        ## move closest to the desired point.
        ## If there is no desired point, this will lead to random walk.

        bestopt = 0
        mindist = 100
        
        for i in range(5): ## try 5 different random options
            cdir = (random.random()-0.5)*.2
            nx = math.cos(self.direction+cdir)
            ny = math.sin(self.direction+cdir)
            d = (nx-target[0])**2+(ny-target[1])**2
            if d < mindist:
                mindist = d
                bestopt = cdir
            #print(cdir,d)

        self.direction+=bestopt

        ## The method does not return anything. Rather, it updates the direction
        ## of this agent.
        
        

def rainbow(x):
    ## Color function that takes a float in the interval [0,1] and returns a color.
    ## 0 = Red, 0.33 = Green, 0.66 = Blue, 1.0 = Red. Between are gradients.
    if x >1:x=1
    if x <0:x=0
    red = math.cos(x*2*math.pi)+0.5
    green = math.cos((x+.66)*2*math.pi)+.05
    blue = math.cos((x+.33)*2*math.pi)+0.5

    outstr = '#'
    for v in [red,green,blue]:
        if v > 1:
            outstr+="ff"
        elif v < 0:
            outstr+="00"
        else:
            h = hex(int(v*255)).split('x')[-1]
            if len(h)==1:
                outstr+="0"+h
            else:
                outstr+=h
    return outstr


def simulate_billiard(arena,n=10,size=10):
    ## Simple billiard simulation without any clash between balls.
    ## This simulation requires an arena (master) in which to play.
    
    ## Create Agents and set their attributes
    agents = []
    for i in range(n):
        agents.append(Ball(arena,size=size))
    for a in agents:
        a.col=rainbow(random.random()) ## Random color
        a.speed=2    ## All balls start with a speed of 2
        a.delay=.001 ## The balls have a small delay of 1 us when displaying. Otherwise,the simulation runs too fast.


    ## Run the simulation until the highest speed on the
    ## billiard table is below 0.5. 
    maxspeed = 2
    while maxspeed>.5:
        for a in agents:
            ## At each point in time, compute the next position of each Ball.
            ## If nx (next x) or ny (next y) is outside the boundaries, deflect the Ball.
            
            nx = a.xpos+a.speed*math.cos(a.direction)
            ny = a.ypos+a.speed*math.sin(a.direction)
            #print(nx,a.xpos,ny,a.ypos)
            if nx>a.limit[2] and nx>a.xpos:
                a.boing(math.pi/2) ## pi/2 is a vertical wall.
            elif nx<a.limit[0] and nx<a.xpos:
                a.boing(math.pi/2)
            elif ny>a.limit[3] and ny>a.ypos:
                a.boing(0)         ## 0 is a horizontal wall.
            elif ny<a.limit[1] and ny<a.ypos:
                a.boing(0)

        ## Determine the highest speed on the board and slow all balls down a little.                
        maxspeed = 0
        for a in agents:
            a.move(step=None)
            a.speed=a.speed*0.999
            if a.speed>maxspeed:maxspeed=a.speed

    return agents



def simulate_chase(hunter=1,prey=1,bystander=0,size=10,zombies=0.0,master=None):
    ## In the chasing scenario, there are three possible types of Humans:
    ## -hunter: These agents hunt prey.
    ## -prey: These agents flee from hunters.
    ## -bystander: These agents don't interact with anyone and just mill around.
    ## The parameter 'zombies' determines the probability with which a prey that
    ## is killed by a hunter turns into a hunter itself.


    ## Determine the size of the playing field
    if master==None:
        h,w=1000,1000
    elif type(master)==list:
        w,h=master[0],master[1]
    else:
        h = master.height
        w = master.width

    ## First create a list of agents. The parameters determine how many agents
    ## of which type are generated.
    ## Each type gets different color and type. The speed of prey is a little faster than
    ## the default 1.0 used for the hunters. This is necessary as they would not stand a
    ## chance against equals in this simple simulation.
    
    agents = []
    for i in range(hunter):
        a = Human(master,size=size)
        a.col="#ff0000"
        a.type="Hunter"
        a.shift()
        agents.append(a)
    for i in range(prey):
        a = Human(master,size=size)
        a.col="#bbff30"
        a.type="Prey"
        a.speed=1.2
        a.shift()
        agents.append(a)
    for i in range(bystander):
        a = Human(master,size=size)
        a.col="#aaaaaa"
        a.type="Bystander"
        a.speed=1.2
        a.shift()
        agents.append(a)


    ## Count the number of prey
    nprey = 0
    for a in agents:
        if a.type=="Prey":nprey+=1
    t=0
    while t < 10000 and nprey>0: ## Run 10000 steps or until there is no prey anymore.
        t+=1
        for a in agents: ## For each agent, find out who they flee from and who they chase.
            seek = []
            flee = []
            if a.type == "Hunter":
                for p in agents:
                    if p.type=="Prey":
                        seek.append(p)
            elif a.type == "Prey":
                for p in agents:
                    if p.type=="Hunter":
                        flee.append(p)
            a.decide(flee,seek)  ## Decide the next step based on these two lists of agents.
            a.move() ## Move the agent in the given direction.


        ## Count the casualties
        deadlist = []
        for i in range(len(agents)):
            if agents[i].type=="Prey": ## For each prey, check whether it was touched by a hunter.
                if agents[i].gotcha(agents,"Hunter"):
                    if random.random()<zombies: ## If a random number in the interval [0,1] is higher than the zombie-probability
                        agents[i].type="Hunter" ## Transform the prey to hunter.
                        agents[i].col="#ff0000"
                    else:    
                        agents[i].kill()        ## If no zombie is generated, just kill the agent and remove it from the agents list.
                        deadlist.append(i)
        for d in deadlist[::-1]:
            agents.pop(d)
            
        nprey=0
        for a in agents: ## Re-Count the number of prey. If it drops to 0, the while-loop ends.
            if a.type=="Prey":nprey+=1
    return agents  ## The final list of all active (not dead) agents is returned and may be evaluated.


def simulate_standoff(n=3,master=None):
    ## Make agents hunting each other. Each agent hunts the one next in line and is hunted by its predecessor.

    ## First create the agents
    agents = []
    for i in range(n):
        a = Human(master,size=10)
        a.col="#8080ff"
        agents.append(a)

    for t in range(10000): ## Run for 10000 ticks
        for i in range(len(agents)): ## For each agent, define the hunter and hunted
            hunt = i+1
            flee = i-1
            if hunt>len(agents)-1:
                hunt=0
            if flee<0:
                flee=-1
            agents[i].decide([agents[flee]],[agents[hunt]]) ## Decide based on the position of hunter and hunted
            agents[i].move()


if __name__ == "__main__":
    
    root = Tk()
    arena = Display(root,800,800)

    #a = simulate_billiard(arena,5,20)
    a = simulate_chase(2,25,0,15,zombies=0.2,master=arena)
    #a = simulate_standoff(10,master=arena)
    root.mainloop()
    

    #### Example for running a simulation without any display
    
    ##a = simulate_chase(2,20,0,10,master=[800,800])
    ##types = {}
    ##for agent in a:
    ##    try:
    ##        types[agent.type]+=1
    ##    except:
    ##        types[agent.type]=1
    ##print("Simulation Finished.")
    ##for t in types.keys():
    ##    print('  '+t+': '+str(types[t]))


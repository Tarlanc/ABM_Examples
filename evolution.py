import random

class GeneticAlgorithm:
    ## This class is a complete genetic algorithm to determine the optimal point of a parameter space.
    def __init__(self, nparam=1, priors=None, psize=50, mutation=0.2, selection=0.6):
        ## nparam: Number of parameters used in the function
        ## priors: Optional priors for each parameter or all parameters. If no prior is used, the prior is N(0,1)
        ## psize: Size of one population of parameter sets.
        ## mutation: Mutation rate for this population (chance to get outlier values)
        ## selection: Selection rate for this population (share of individuals to be killed after each step)
        ##
        ## **NOTE: The higher the mutation and the lower the selection, the slower the
        ##         convergence and the lower the risk of homing in on local optima.
        
        self.paramspace = []
        self.psize = psize
        self.mutation = mutation
        self.selection = selection
        self.history = {'Param':[self.paramspace],'Result':[]}
        self.eta=0.0001 ## Convergence criterium. A normal evolution stops if all results lie within an interval of breadth eta.
        self.maxgen=50  ## Usual maximal number of generations.

        ## Set up an initial parameter space (priors for the distribution of each parameter)        
        if type(priors) == list:
            if len(priors)==nparam:
                for e in priors:
                    if type(e)==tuple:
                        self.paramspace.append(e)
                    elif type(e) in [int,float]:
                        self.paramspace.append((e,1))
        elif type(priors) == tuple:
            for i in range(nparam):
                self.paramspace.append(priors)
        else:
            for i in range(nparam):
                self.paramspace.append((0,1))

        ## Generate an intial population of parameter sets.
        ## Each has random values for each parameter.
        self.population = []
        for i in range(psize):
            self.population.append(self.create_individual())

    def create_individual(self):
        ## Generate one random parameter set in the confines of the parameter space
        ind = []
        for p in self.paramspace:
            mut = random.random()<self.mutation
            if mut:
                ind.append(random.normalvariate(p[0],p[1]*2))
            else:
                ind.append(random.normalvariate(p[0],p[1]))
        return ind

    def m_sd(self,l):
        ## Assisting function to compute Mean and Standard Deviation of a list of values.
        ## Used in the estimation of posterior parameter space and in the output.
        m = float(sum(l))/len(l)
        qs = 0.0
        for e in l:
            qs+=(e-m)**2
        sd = (qs/(len(l)-1))**.5
        return (m,sd)

    def update_params(self):
        ## Update the parameter space, based on the currently living individuals.
        table = []
        np = len(self.paramspace)
        for p in range(np):
            table.append([])
        for ind in self.population:
            for i in range(np):
                table[i].append(ind[i])

        for i in range(np):
            self.paramspace[i]=self.m_sd(table[i])
        self.history['Param'].append(self.paramspace)

    def optimize(self,funct,*args):
        ## Do one evolutionary step, consisting of testing each individual, killing a fixed
        ## share of underachievers, reassessing the parameter spaces based on survivors, and
        ## generation of new offspring.
        ## This step may be repeated in loops.
        ##
        ## The method takes a function and a list of arguments that should be passed to this
        ## function before appending the parameters. The parameters are passed to the function
        ## in the form of a list.

        ## Test each individual
        ranking = []
        for ind in self.population:
            result = funct(*args,ind)
            ranking.append((result,ind))
        ranking = sorted(ranking,reverse=True)

        self.history['Result'].append(ranking)

        ## Kill off the share specified in self.selection
        newpop = []
        nretain = int(len(ranking)*(1-self.selection))
        for r in ranking[:nretain]:
            newpop.append(r[1])
        self.population = newpop

        ## Re-Assess the parameter space
        self.update_params()

        ## Repopulate the population
        for i in range(len(self.population),self.psize):
            self.population.append(self.create_individual())
        return ranking

    def evolve(self,funct,*args):
        ## Macro-Evolution using several steps to achieve an optimal solution.
        ## There are two abort conditions: The maximum number of generations (self.maxgen) is reached
        ## or the results vary by less than self.eta. In both cases, the evolution ends.
        gen = 1
        goal = False
        while not goal:
            r = sorted(self.optimize(funct,*args))
            eta = abs(r[0][0]-r[-1][0])
            if gen>self.maxgen or eta<self.eta:
                goal=True
            gen+=1

    def write_history(self,fname=None):
        ## Output of the evolutionary history.
        ## For the results and each parameter, the descriptives in each generation are shown.
        ## If a filename is specified, the results are written to a tab-spaced textfile.
        ## The results are also returned as a dictionary with the variable names as keys and the data as numeric lists.
        
        generations = len(self.history['Result'])
        parameters = len(self.paramspace)

        try:
            outf = open(fname,'w')
            file = True
        except:
            file = False

        vnames = ['Generation','Result_M','Result_SD','Result_Min','Result_Max']
        for i in range(parameters):
            vnames+=['Param_{0:02}_M'.format(i+1),
                     'Param_{0:02}_SD'.format(i+1),
                     'Param_{0:02}_Max'.format(i+1),
                     'Param_{0:02}_Min'.format(i+1)]

        if file: outf.write('\t'.join(vnames)+'\n')
        outdic ={}
        for v in vnames:
            outdic[v]=[]

        for gen in range(generations):
            values = [str(gen)]
            nvalues = [gen]
            res = list(list(zip(*self.history['Result'][gen]))[0])
            desc = self.m_sd(res)
            values+=[str(desc[0]),str(desc[1]),str(max(res)),str(min(res))]
            nvalues+= [desc[0],desc[1],max(res),min(res)]
            for i in range(parameters):
                res = []
                for e in self.history['Result'][gen]:
                    res.append(e[1][i])
                desc = self.m_sd(res)
                values+=[str(desc[0]),str(desc[1]),str(max(res)),str(min(res))]
                nvalues+= [desc[0],desc[1],max(res),min(res)]

            for i in range(len(vnames)):
                outdic[vnames[i]].append(nvalues[i])

            if file: outf.write('\t'.join(values)+'\n')
        if file: outf.close()
        return outdic

    def bestguess(self):
        ## This method just returns the best current estimation of optimal parameters.
        if len(self.history['Result'])>0:
            bg = self.history['Result'][-1][0]
        return bg[1]

    def age(self):
        ## This method just returns the number of passed generations.
        return len(self.history['Result'])
            
            
## The function below is a very simple problem to be solved by an evolutionary algorithm.
## The problem is to find the minimum of the equation: Value = (u+a)**2 + (v+b)**2 + (w+c)**2
## Where a, b, and c are given in the model specification. The algorithm has to find the optimal
## values for u,v,w.
## As this function has its minimum exactly at the point where each summand equals zero (u == -a, v == -b, w == -c),
## it is quite easy to guess the correct result.
## Since the GeneticAlgorithm looks for the highest possible result, the result is inverted, here.
    
def simulation(model=[1,2,3],parlist=[0,0,0]):
    u,v,w = parlist[0],parlist[1],parlist[2]
    result = (u+model[0])**2 + (v+model[1])**2 + (w+model[2])**2 ## Compute the value
    result = 0-result ## Invert the value, so the minimum becomes the maximum.
    return result


if __name__ == "__main__":
    
    ## Example usage:
    ## --------------


    
    ## Set up a genetic algorithm with three parameters
    g = GeneticAlgorithm(3)

    ## Run the algorithm for 50 generations
    for gen in range(50):
        g.optimize(simulation,[1,2,3])

    ## Get the currently best result
    print(g.bestguess())

    ## Get the number of generations used in this evolution
    print(g.age())

    ## Get the complete history as a dictionary
    table = g.write_history()

    ## Print the 50 results to see how close the algorithm got to the optimum (=0).
    print(table['Result_M'])


    ## Set up another genetic algorithm with three parameters
    g2 = GeneticAlgorithm(3)

    ## Let it evolve on a different problem. It will terminate once it reaches convergence or the maximal number of generations.
    g2.evolve(simulation,[3,2,1])

    ## Get the currently best result and the number of generations
    print(g2.bestguess())
    print(g2.age())

    ## Write the history to a file to inspect later.
    g.write_history('test.xls')
    
    
        

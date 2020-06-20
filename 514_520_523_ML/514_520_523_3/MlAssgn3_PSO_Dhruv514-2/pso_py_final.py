import random
import numpy as np
import matplotlib.pyplot as plt
iter_no=10
p_no=50
error_val=0.1
targetval=-19.2 #CHANGE ACCORDING TO MINIMA OF RESPECTIVE FUNC (-959 and -19.2)
area_bound=10 #USE 512 for eggholder and 10 for holdertable

plot_gbestval=np.zeros(iter_no)
plot_avgval=np.zeros(iter_no)

c0=0.5
c1=0.3
c2=0.4

def eggholder(x,y):
    
    return -(y+47)*np.sin(np.sqrt(abs(y+x/2.0+47)))-x*np.sin(np.sqrt(abs(x-(y+47))))
    
def holdertable(x,y):
    
    return -abs(np.sin(x)*np.cos(y)*np.exp(abs(1-np.sqrt(x**2+y**2)/np.pi)))

class Particle():
    def __init__(self):
        self.pos=np.array([random.randint(-area_bound,area_bound),random.randint(-area_bound,area_bound)])
        self.bestp=self.pos
        self.vel=np.array([0,0])
        self.bestval=float('inf')
        
    def move(self):
        self.pos=self.pos+self.vel
        
        
class PSO():
    
    def __init__(self,t,error_val,p_no):
        self.t=t
        self.error_val=error_val
        self.p_no=p_no
        self.plist=np.array([])
        self.globalbest=float('inf')
        self.globalbpos=np.array([random.randint(-area_bound,area_bound),random.randint(-area_bound,area_bound)])
        
    def fitnessfunc(self,p):
        
        #CHANGE FUNCTION NAME HERE
        
        return holdertable(p.pos[0],p.pos[1])
        
    def pbest(self):
        for a in self.plist:
            p0=self.fitnessfunc(a)
            if(a.bestval>p0):
                a.bestval=p0
                a.bestp=a.pos
                
    def gbestval(self):
        for p in self.plist:
            fitmax=self.fitnessfunc(p)
            if(self.globalbest>fitmax):
                self.globalbest=fitmax
                self.globalbpos=p.pos
                
    def global_move(self):
        for p in self.plist:
            vel1=c0*p.vel+c1*random.random()*(p.bestp-p.pos)+c2*random.random()*(self.globalbpos-p.pos)
            p.vel=vel1
            p.move()
            
pso_run=PSO(targetval,error_val,p_no)

particlelist=[Particle() for i in range(p_no)]

pso_run.plist=particlelist




for i in range(iter_no):
    pso_run.gbestval()
    pso_run.pbest()
    
    if(abs(pso_run.globalbest-pso_run.t)<=error_val):
        break
    pso_run.global_move()
    plot_gbestval[i]=pso_run.globalbest
    plot_avgval[i]=np.mean([p.bestval for p in pso_run.plist])
    
plt.plot(plot_gbestval)
plt.plot(plot_avgval)
    
    
print(pso_run.globalbpos,pso_run.globalbest)














            
                
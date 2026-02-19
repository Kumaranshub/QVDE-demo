import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("dark_background")

# ---------------- ENERGY FUNCTIONAL ----------------
def energy(x,y):
    smooth = 0.6*(x**2+y**2)
    oscill = 0.8*np.sin(2.5*x)*np.cos(2.5*y)
    ridge  = 0.25*np.sin(x*y)
    return smooth + oscill + ridge

def grad(p):
    x,y=p
    gx=1.2*x + 2*np.cos(2.5*x)*np.cos(2.5*y) + 0.25*y*np.cos(x*y)
    gy=1.2*y - 2*np.sin(2.5*x)*np.sin(2.5*y) + 0.25*x*np.cos(x*y)
    return np.array([gx,gy])

# ---------------- SIMULATION PARAMETERS ----------------
particles=6
steps=260
dt=0.03
eta=0.35

def simulate(noise_level):
    trajs=[]
    energies=[]
    phases=[]
    for _ in range(particles):
        pos=np.random.uniform(-2,2,2)
        vel=np.random.randn(2)*0.2
        
        traj=[pos.copy()]
        en=[energy(pos[0],pos[1])]
        ph=[vel.copy()]
        
        for _ in range(steps):
            force=-grad(pos)
            noise=noise_level*np.random.randn(2)
            acc=force-eta*vel+noise
            vel+=acc*dt
            pos+=vel*dt
            
            traj.append(pos.copy())
            en.append(energy(pos[0],pos[1]))
            ph.append(vel.copy())
            
        trajs.append(np.array(traj))
        energies.append(np.array(en))
        phases.append(np.array(ph))
        
    return trajs,energies,phases

traj_det,en_det,ph_det=simulate(0.0)
traj_sto,en_sto,ph_sto=simulate(0.04)

# ---------------- ENERGY SURFACE ----------------
x=np.linspace(-2,2,150)
y=np.linspace(-2,2,150)
X,Y=np.meshgrid(x,y)
Z=energy(X,Y)

# ---------------- FIGURE LAYOUT ----------------
fig=plt.figure(figsize=(14,10))

axL=fig.add_subplot(221,projection='3d')
axR=fig.add_subplot(222,projection='3d')
axE=fig.add_subplot(223)
axP=fig.add_subplot(224)

for ax,title in zip([axL,axR],
                    ["Deterministic Dynamics",
                     "Stochastic Dynamics"]):
    ax.plot_surface(X,Y,Z,cmap="inferno",alpha=0.7)
    ax.set_title(title)

axE.set_title("Energy Convergence")
axE.set_xlabel("Time")
axE.set_ylabel("Energy")

axP.set_title("Phase Portrait")
axP.set_xlabel("Position X")
axP.set_ylabel("Velocity X")

# ---------------- OBJECTS ----------------
linesL=[];pointsL=[]
linesR=[];pointsR=[]
linesE=[];phasePts=[]

for _ in range(particles):
    l1,=axL.plot([],[],[],lw=3)
    p1,=axL.plot([],[],[],'o')
    l2,=axR.plot([],[],[],lw=3)
    p2,=axR.plot([],[],[],'o')
    le,=axE.plot([],[])
    ph,=axP.plot([],[],'o',ms=3)
    
    linesL.append(l1);pointsL.append(p1)
    linesR.append(l2);pointsR.append(p2)
    linesE.append(le);phasePts.append(ph)

# ---------------- UPDATE FUNCTION ----------------
def update(frame):

    axL.view_init(35,frame*1.2)
    axR.view_init(35,-frame*1.2)

    for i in range(particles):

        if frame<len(traj_det[i]):

            # deterministic surface traj
            xs=traj_det[i][:frame+1,0]
            ys=traj_det[i][:frame+1,1]
            zs=energy(xs,ys)
            linesL[i].set_data(xs,ys)
            linesL[i].set_3d_properties(zs)

            px,py=traj_det[i][frame]
            pz=energy(px,py)
            pointsL[i].set_data([px],[py])
            pointsL[i].set_3d_properties([pz])

            # stochastic traj
            xs=traj_sto[i][:frame+1,0]
            ys=traj_sto[i][:frame+1,1]
            zs=energy(xs,ys)
            linesR[i].set_data(xs,ys)
            linesR[i].set_3d_properties(zs)

            px,py=traj_sto[i][frame]
            pz=energy(px,py)
            pointsR[i].set_data([px],[py])
            pointsR[i].set_3d_properties([pz])

            # energy graph
            linesE[i].set_data(range(frame+1),
                               en_det[i][:frame+1])

            # phase portrait
            vx=ph_det[i][:frame+1,0]
            px=traj_det[i][:frame+1,0]
            phasePts[i].set_data(px,vx)

    axE.relim();axE.autoscale_view()
    axP.relim();axP.autoscale_view()

    return linesL+pointsL+linesR+pointsR+linesE+phasePts

ani=FuncAnimation(fig,update,frames=steps,interval=40)

# ---------- EXPORTS ----------
ani.save("qvde_final.mp4",writer="ffmpeg",fps=30,dpi=250)
fig.savefig("qvde_paper_figure.png",dpi=350)

print("FINAL VIDEO: qvde_final.mp4")
print("PAPER FIGURE: qvde_paper_figure.png")

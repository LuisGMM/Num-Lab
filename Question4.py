
import numpy as np
import matplotlib.pyplot as plt

from algorithm import get_T_density

dt = 0.005
tf = 50 
dx = 0.05 
xmin = -60 
xmax = 60 
k0 = 1
sigma0 = 3
x0 = -10
L = 2
V0 = 2
M = 2401

def start_plot():
    
    global fig, ax, line

    fig = plt.figure()
    ax = plt.axes(xlim=(0, 10), ylim=(0, 1.001))
    line, = ax.plot([], [])

def E0(k0_:float, sigma0_:float = sigma0)->float: return (k0_**2 + 1/(2*sigma0_**2))/2 

def T_theoretical(E:float)->float:
    return (1 + (V0**2)/(4*E*(V0-E))*np.sinh(L*np.sqrt(2*(V0-E)))**2)**(-1) if (E < V0) else (1 + (V0**2)/(4*E*(E-V0))*np.sin(L*np.sqrt(2*(E-V0)))**2)**(-1)

def T_experimental(filename:str)->float:
    # return get_T_density(psi_density=np.load(filename))[-1]
    return np.amax(get_T_density(psi_density=np.load(filename)))


def run() -> None:

    start_plot()

    E_i_space = [E0(k0) for k0 in np.arange(0.5,8,0.5)] # May be wrong?
    E_space = np.arange(0,10,0.001)

    try:
        t = np.load('T_experimental.npy')
        T_theo = np.load('T_theoretical.npy')
    except:
        t = np.array([T_experimental(f'psi_{k0}.npy') for k0 in np.arange(0.5,8,0.5)])
        T_theo = np.array([T_theoretical(E) for E in E_space])
        
        np.save('T_experimental.npy', t)
        np.save('T_theoretical.npy', T_theo)

    plt.plot(E_i_space, t, '-o', color='red', label='wave packet')  # I have to plot the experimental ponts not the theoretical ones
    plt.plot(E_space, T_theo, color='blue', label=r'$T(E)$')  
    
    plt.xlabel('$Energy(E_0)$')
    plt.ylabel('$T(E)$')
    plt.title("")
    plt.legend()  
    plt.show()




if __name__ == '__main__':

    # E_i_space = [E0(k0) for k0 in np.arange(0.5,8,0.5)] # May be wrong?
    # E_space = np.arange(0,10,0.001)

    # T_exp = np.array([T_experimental(f'psi_{k0}.npy') for k0 in np.arange(0.5,8,0.5)])
    # T_theo = np.array([T_theoretical(E) for E in E_space])
    
    # np.save('T_experimental.npy', T_exp)
    # np.save('T_theoretical.npy', T_theo)
    
    run()
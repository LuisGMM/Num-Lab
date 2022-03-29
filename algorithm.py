
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation


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

i = 1j

N = int((10/k0)/dt) # Round to the nearest integer number

N = 10000 # Override Number of iterations to get more data

alpha = dt / ( 4 * dx **2 )
beta = 1 + 2*i*alpha
a = -alpha*i # Subdiagonal element of L matrix

def d(j:int)->complex: # Diagonal element of L matrix. From 1 to M 
    return beta + i*dt*V(x(j))/2

def V(x:float, L:float = L, V0:float = V0)->float:  # What happens when x==0 or x==L ?
    return 0 if x < 0 or x > L else V0

def x(j:int, xmin:float = xmin, dx:float = dx)->float:
    return xmin + (j-1)*dx

def t(k:int, dt:float = dt)->float: # Something is wrong here because the last element is 9.99 instead of tf (==50)
    return (k-1)*dt

def psi_0(x:float, k0_:float = k0)->complex:  
    return np.power((1/( np.pi * sigma0**2 ) ), 1/4)*np.exp( i*k0_*x )*np.exp(-( (x-x0)**2 / (2*sigma0**2) ))

a_dev_cache = {}
def a_dev(j:int)->complex:
    a_dev_cache[j] = (a/d(j)) if j==1 else (a/(d(j) - a*a_dev_cache[j-1]))    
    return a_dev_cache[j]

s_dev_cache = {}
def s_dev(j:int, s:np.array, a_dev:np.array)->complex:
    s_dev_cache[j] = (s[j-1]/d(j)) if j==1 else ( (s[j-1] -a*s_dev_cache[j-1] )/( d(j) -a*a_dev[(j-1)-1] ) ) 
    return s_dev_cache[j]

x_next_cache = {}
def x_next(j:int, s_dev:np.array, a_dev:np.array)->complex:
    x_next_cache[j] = s_dev[j-1] if j==(M) else ( s_dev[j-1] - a_dev[j-1]*x_next_cache[j+1] )
    return x_next_cache[j]

def probability_density(psi:np.array):
    return psi.conjugate()*psi

def check_psi_stability(psi: np.array, dx:float = dx)-> float:
    temp_psi__square_k = probability_density(psi=psi)
    temp_psi__square_k[0] /= 2 
    return dx * (sum(temp_psi__square_k))


R = np.zeros((M,M), dtype=np.complex)

np.fill_diagonal(R, [ beta.conjugate() - i*dt*V( x(j))/2 for j in range(M) ]) # Revise this
R[ [i+1 for i in range(M-1)], [i for i in range(M-1)] ] = i*alpha #Modifying the subdiagonal                 
R[ [i for i in range(M-1)], [i+1 for i in range(M-1)] ] = i*alpha #Modifying the superdiagonal

L = R.conjugate()


v_x = np.array([x(j) for j in range(1, M+1)]) # Store all positions
v_t = np.array([t(k) for k in range(1, N+1)]) # Store all times


def get_all_states(k0_:float = k0, N_:int = N, save_stability=False, save_density_function=True, filename_density_function='psi.npy', filename_stability='psi_stability.npy'):

    psi_temp = np.array([psi_0(x, k0_) for x in v_x])    
    psi_temp_density = probability_density(psi=psi_temp)

    v_stability = np.zeros((M))
    v_stability[0] = check_psi_stability(psi=psi_temp)

    m_psi = np.zeros((M,N_))
    m_psi[:, 0] = psi_temp_density

    for k in range(1,N_):
        
        s_trid = R.dot(psi_temp)

        v_a_dev = np.array([a_dev(j) for j in range(1, M)]) # Store all recursive a'
        v_s_dev = np.array([s_dev(j, s=s_trid, a_dev=v_a_dev) for j in range(1, M+1)]) # Store all recursive s'
        
        psi_temp = np.array([x_next(j, s_dev=v_s_dev, a_dev=v_a_dev) for j in range(M, 0, -1)])[::-1]
        psi_temp_density = probability_density(psi=psi_temp)
        
        m_psi[:, k] = psi_temp_density
    
        if k<=2400: 
            v_stability[k] = check_psi_stability(psi=psi_temp)
        # stability = np.array([check_psi_stability(psi=psi_density) for psi_density in m_psi[:, ]])        
    if save_stability:
        np.save(filename_stability, v_stability)

    if save_density_function:
        np.save(filename_density_function, m_psi)    
    
    return m_psi, v_stability

def get_T_probability(psi_density_at_k:np.array, x:np.array = v_x, dx:float = dx)-> float:
    # np.where(...)... == Getting the index at which the position of the density is 0
    temp_psi__square_k = psi_density_at_k[np.where(x==2)[0][0]:]
    temp_psi__square_k[0] /= 2 
    return dx * (sum(temp_psi__square_k))

def get_T_density(psi_density:np.array, x:np.array = v_x, dx:float = dx)-> np.array:
    return np.array([get_T_probability(psi_density_at_k=psi_density[:,i], x=x, dx=dx) for i in range(psi_density.shape[1])])    




##############################   Sketchy method, DO NOT USE   ##############################

def get_next_state():

    v_x = np.array([x(j) for j in range(1, M+1)]) # Store all positions
    v_t = np.array([t(k) for k in range(1, N+1)]) # Store all times

    psi_current = np.array([psi_0(x) for x in v_x])    
    psi_current_density = probability_density(psi=psi_current)
    
    # plt.plot(v_x, psi_current_density, color="g")
    # plt.show()
    
    s_trid = R.dot(psi_current)

    v_a_dev = np.array([a_dev(j) for j in range(1, M)]) # Store all recursive a'
    v_s_dev = np.array([s_dev(j, s=s_trid, a_dev=v_a_dev) for j in range(1, M+1)]) # Store all recursive s'
    psi_next = np.array([x_next(j, s_dev=v_s_dev, a_dev=v_a_dev) for j in range(M, 0, -1)])

    print("\n \n", psi_current.shape, v_s_dev.shape, psi_next.shape, "\n \n")   
    print(check_psi_stability(psi=psi_next), "\n \n")




if __name__ == '__main__':
    get_all_states(save_stability=True, save_density_function=True)

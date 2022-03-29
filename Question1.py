
from algorithm import *

from matplotlib.patches import Rectangle


def start_plot():
    
    global fig, ax, line

    fig = plt.figure()
    ax = plt.axes(xlim=(-30, 30), ylim=(0, 0.5))
    line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,

def animate(i, *fargs):
    line.set_data(fargs[0], fargs[1][:, i])
    return line,

def run(k0:float = 1.0):

    start_plot()

    try:
        psi = np.load(f'psi_{k0}.npy') # 99.99%+ Stability
    
    except:
        psi = get_all_states(filename_density_function=f'psi_{k0}.npy')[0]

    plt.rc('font', family='Computer Modern')

    potential, = ax.plot(v_x, [V(x) for x in v_x])

    potential.set_label(r'$V(x)$')
    line.set_label(r'$\left| \Psi(x, t) \right|^2$')

    plt.xlabel("X")
    plt.ylabel(r"$\left| \Psi(x) \right|^2$")
    # plt.title(r'$\Psi(x)$')

    ax.legend()
    ax.add_patch( Rectangle((0,0), 2, 2, color='orange', linewidth=0, alpha=0.5) )
    anim = animation.FuncAnimation(fig, animate, fargs=[v_x, psi], init_func=init, frames=N, interval=dt, blit=True)
    plt.show()


def plot(k0):


    start_plot()

    try:
        psi = np.load(f'psi_{k0}.npy') # 99.99%+ Stability
    
    except:
        psi = get_all_states(filename_density_function=f'psi_{k0}.npy')[0]

    potential, = ax.plot(v_x, [V(x) for x in v_x])

    potential.set_label(r'$V(x)$')

    plt.xlabel("X")
    plt.ylabel(r"$\left| \Psi(x) \right|^2$")
    # plt.title(r'$\Psi(x)$')

    
    ax.add_patch( Rectangle((0,0), 2, 2, color='orange', linewidth=0, alpha=0.5) )

    plt.plot(v_x, psi[:, 0], color="black", label='Initial packet')
    plt.plot(v_x, psi[:, 500], color="red", label='$500 \Delta t$')
    plt.plot(v_x, psi[:, 1000], color="green", label='$1000 \Delta t$')
    plt.plot(v_x, psi[:, 1500], color="blue", label='$1500 \Delta t$')
    plt.plot(v_x, psi[:, 2000], color="purple", label='$2000 \Delta t$')

    ax.legend()

    plt.show()



if __name__ == '__main__':

    # psi = np.load('psi_1.0.npy') # 99.99%+ Stability


    # plt.rc('font', family='Computer Modern')

    # potential, = ax.plot(v_x, [V(x) for x in v_x])

    # potential.set_label(r'$V(x)$')
    # line.set_label(r'$\left| \Psi(x, t) \right|^2$')

    # plt.xlabel("X")
    # plt.ylabel(r"$\left| \Psi(x) \right|^2$")
    # # plt.title(r'$\Psi(x)$')

    # ax.legend()
    # ax.add_patch( Rectangle((0,0), 2, 2, color='orange', linewidth=0, alpha=0.5) )
    # anim = animation.FuncAnimation(fig, animate, fargs=[v_x, psi], init_func=init, frames=N, interval=dt, blit=True)
    # plt.show()
    
    # ax = plt.axes(xlim=(0, 60), ylim=(0, 0.05))
    # T_plot, = ax.plot(v_t, v_T_density)
    # plt.show()

    run(1.0)




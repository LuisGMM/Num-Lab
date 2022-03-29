
from datetime import datetime
from matplotlib.patches import Rectangle
from algorithm import *


def start_plot():
    
    global fig, ax, line

    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 15), ylim=(0, 0.005))
    line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,

def animate(i, *fargs):
    line.set_data(fargs[0], fargs[1][:, i])
    return line,

def update_title(axes):
    axes.set_title(datetime.now())
    axes.figure.canvas.draw()

# Or could start the timer on first figure draw:
def start_timer(event):
    timer.start()
    fig.canvas.mpl_disconnect(drawid)

def graph_1(psi_filename):

    global timer, drawid, anim 

    start_plot()

    try:
        psi = np.load(psi_filename) # 99.99%+ Stability
    except:
        psi = get_all_states(filename_density_function=psi_filename)[0]

    timer = fig.canvas.new_timer(interval=100)
    timer.add_callback(update_title, ax)
    # timer.start()
    drawid = fig.canvas.mpl_connect('draw_event', start_timer)

    potential, = ax.plot(v_x, [V(x) for x in v_x])
    potential.set_label(r'$V(x)$')
    line.set_label(r'$\left| \Psi(x, t) \right|^2$')

    plt.xlabel("X")
    plt.ylabel(r'$\left| \Psi(x) \right|^2$')
    # plt.title(r'$\Psi(x)$')
    ax.legend()
    ax.add_patch( Rectangle((0,0), 2, 2, color='orange', linewidth=0, alpha=0.5) )
    anim = animation.FuncAnimation(fig, animate, fargs=[v_x, psi], init_func=init, frames=N, interval=dt, blit=True)
    # plt.show()

def graph_2(psi_filename, ylim=0.005, color='black', label=None, axhline=False, title=''):

    global ax, T_plot

    start_plot()

    try:
        psi = np.load(psi_filename) # 99.99%+ Stability    
    except:
        psi = get_all_states(filename_density_function=psi_filename)[0]

    v_T_density = get_T_density(psi, x=v_x)   

    # ax = plt.axes(xlim=(0, 60), ylim=(0, ylim))
    # ax = plt.axes()

    if ylim==0.005 and '1.0' in psi_filename:
        ax = plt.axes(xlim=(0, 60), ylim=(0, ylim))
    else:
        ax = plt.axes()
        plt.yscale("log")

    T_plot, = ax.plot(v_t, v_T_density, color=color, label=label)

    if axhline:
        ax.axhline(y=0.00373, color=color, linestyle='--', label=r'$T \to 0.0037$')
    
    plt.title(title)
    plt.ylabel('Transmission probability')
    plt.xlabel('Time')

    ax.legend()

def plot():

    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 15), ylim=(0, 0.005))

    psi = np.load('psi_1.0.npy')

    potential, = ax.plot(v_x, [V(x) for x in v_x])
    potential.set_label(r'$V(x)$')

    plt.xlabel("X")
    plt.ylabel(r'$\left| \Psi(x) \right|^2$')
    # plt.title(r'$\Psi(x)$')
    ax.add_patch( Rectangle((0,0), 2, 2, color='orange', linewidth=0, alpha=0.5) )

    plt.plot(v_x, psi[:, 0], color="black", label='Initial packet')
    plt.plot(v_x, psi[:, 500], color="red", label='$500 \Delta t$')
    plt.plot(v_x, psi[:, 1000], color="green", label='$1000 \Delta t$')
    plt.plot(v_x, psi[:, 1500], color="blue", label='$1500 \Delta t$')
    plt.plot(v_x, psi[:, 2000], color="violet", label='$2000 \Delta t$')

    ax.legend()

    plt.show()


    
def run_graph1(psi_filename) -> None:
    graph_1(psi_filename)
    plt.show()

def run_graph2(psi_filename, ylim=0.005, color='black', label=None, axhline=False, title='') -> None:
    graph_2(psi_filename, ylim=0.005, color='black', label=None, axhline=False, title='')
    plt.show()


if __name__ == '__main__':
 
    # graph_2('psi_1.0.npy', ylim=0.005, axhline=True, color="red")
    # # graph_1('psi.npy')

    # plt.show()

    plot()
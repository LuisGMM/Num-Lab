
import random as r

from algorithm import *

from Question2 import graph_2, start_plot


def new_color():
    return r.randint(500,8000)/8000

def run() -> None:

    start_plot()

    for i in np.arange(0.5,8,0.5):
       graph_2(f'psi_{i}.npy', ylim=1, color=(new_color(), new_color(), new_color()), label=f'$k_0$ - {i}', axhline=False)

    plt.show()



if __name__ =='__main__':
    run()

# %%
import matplotlib.pyplot as plt
import numpy as np
from radiocores.qammod import qammod as qm


def show_constellation(order, distance):
    annotation_format = "0" + str(int(np.log2(order))) + "b"
    x = np.arange(order)
    points = [qm(x_i, order, distance) for x_i in x]

    for i, point in enumerate(points):
        plt.scatter(point.real, point.imag, color="blue")
        plt.annotate(format(x[i], annotation_format), (point.real, point.imag))

    plt.show()


# %%
order = 64
distance = 2
show_constellation(order, distance)
# %%

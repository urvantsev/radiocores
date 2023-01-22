import numpy as np

M = 16
a = 45
b = a

for i in range(0, np.log2(M).astype(int) - 1):
    a, b = (lambda x, y: (x >> 1, y ^ (x >> 1)))(a, b)

print("%d\n" % (b))

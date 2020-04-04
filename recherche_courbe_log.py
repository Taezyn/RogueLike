import numpy as np
import matplotlib.pyplot as plt

C = np.linspace(1, 5, 5)
N = np.linspace(1, 15, 15)
M = []
for c in C:
    m = []
    for n in N:
        m.append(int(c*np.log(n))+1)
    M.append(m)

for c in C:
    plt.plot(N, M[int(c)-1], label=str(c))
    
plt.grid()
plt.legend()
plt.show()

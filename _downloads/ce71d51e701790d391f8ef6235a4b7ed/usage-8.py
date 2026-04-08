import matplotlib.pyplot as plt
import numpy as np
from cline import Cline

L = Cline.from_line(0, 1+1j)  # line y = x

fig, ax = plt.subplots(figsize=(8, 8))
t = np.linspace(-4, 4, 100)
ax.plot(t, t, 'k--', alpha=0.4, label='Line y = x')

points = [3+0j, 1+3j, -1+2j, 2-1j]
for z in points:
    z_ref = L.invert(z)
    ax.plot(z.real, z.imag, 'bo', markersize=8)
    ax.plot(z_ref.real, z_ref.imag, 'ro', markersize=8)
    ax.plot([z.real, z_ref.real], [z.imag, z_ref.imag], 'gray', alpha=0.4, linestyle=':')

ax.plot([], [], 'bo', label='Original points')
ax.plot([], [], 'ro', label='Reflected points')
ax.set_xlim(-3, 5)
ax.set_ylim(-3, 5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title('Point reflection in a line')
import matplotlib.pyplot as plt
import numpy as np
from cline import Cline

S = Cline.from_circle(center=0, radius=2)
theta = np.linspace(0, 2*np.pi, 100)

fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(S.radius*np.cos(theta), S.radius*np.sin(theta), 'k--', alpha=0.4, label='Inversion circle (r=2)')

points = [3+1j, 1+0.5j, 4+2j, 0.5+1.5j]
for z in points:
    z_inv = S.invert(z)
    ax.plot(z.real, z.imag, 'bo', markersize=8)
    ax.plot(z_inv.real, z_inv.imag, 'ro', markersize=8)
    ax.annotate('', xy=(z_inv.real, z_inv.imag), xytext=(z.real, z.imag),
                arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))

ax.plot([], [], 'bo', label='Original points')
ax.plot([], [], 'ro', label='Inverted points')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title('Point inversion in a circle')
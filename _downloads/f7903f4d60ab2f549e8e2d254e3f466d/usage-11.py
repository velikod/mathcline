import matplotlib.pyplot as plt
import numpy as np
from cline import Cline

S = Cline.from_circle(center=0, radius=1)
L = Cline(c=0, alpha=1+0j, d=-2)  # vertical line x=1
L_img = S.invert(L)

fig, ax = plt.subplots(figsize=(8, 8))
theta = np.linspace(0, 2*np.pi, 100)

# Inversion circle
ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Inversion circle')
# Original line x=1
ax.axvline(x=1, color='b', label='Original line x=1')
# Image circle (passes through origin)
ax.plot(L_img.center.real + L_img.radius*np.cos(theta),
        L_img.center.imag + L_img.radius*np.sin(theta), 'r', label='Image circle')

ax.set_xlim(-1.5, 2.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title('Line → Circle (line not through center)')
import matplotlib.pyplot as plt
import numpy as np
from cline import Cline

S = Cline.from_circle(center=0, radius=1)
C = Cline.from_circle(center=1, radius=1)  # passes through origin
C_img = S.invert(C)

fig, ax = plt.subplots(figsize=(8, 8))
theta = np.linspace(0, 2*np.pi, 100)

# Inversion circle
ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Inversion circle')
# Original circle (through origin)
ax.plot(1 + np.cos(theta), np.sin(theta), 'b', label='Original circle (through 0)')
# Image line
x_line = np.full(100, 0.5)
y_line = np.linspace(-3, 3, 100)
ax.plot(x_line, y_line, 'r', label=f'Image line')

ax.set_xlim(-2, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title('Circle → Line (circle through center)')
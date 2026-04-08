import matplotlib.pyplot as plt
import numpy as np
from cline import Cline

S = Cline.from_circle(center=0, radius=1)
L = Cline.from_line(-1, 1)  # real axis, through origin
L_img = S.invert(L)

fig, ax = plt.subplots(figsize=(8, 8))
theta = np.linspace(0, 2*np.pi, 100)

# Inversion circle
ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Inversion circle')
# Original and image (both the real axis)
ax.axhline(y=0, color='b', linewidth=2, label='Line through center (fixed)')

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title('Line → Line (line through center)')
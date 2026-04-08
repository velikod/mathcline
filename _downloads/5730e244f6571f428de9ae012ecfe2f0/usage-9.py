import matplotlib.pyplot as plt
import numpy as np
from cline import Cline

S = Cline.from_circle(center=0, radius=2)
C = Cline.from_circle(center=3, radius=1)
C_img = S.invert(C)

fig, ax = plt.subplots(figsize=(8, 8))
theta = np.linspace(0, 2*np.pi, 100)

# Inversion circle
ax.plot(S.radius*np.cos(theta), S.radius*np.sin(theta), 'k--', alpha=0.3, label='Inversion circle')
# Original
ax.plot(C.center.real + C.radius*np.cos(theta),
        C.center.imag + C.radius*np.sin(theta), 'b', label='Original circle')
# Image
ax.plot(C_img.center.real + C_img.radius*np.cos(theta),
        C_img.center.imag + C_img.radius*np.sin(theta), 'r', label='Image circle')

ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title('Circle → Circle (not through center)')
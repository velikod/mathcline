import matplotlib.pyplot as plt
import numpy as np
from cline import Cline

S = Cline.from_circle(center=0, radius=1)
theta = np.linspace(0, 2*np.pi, 300)
ks = [-3, -2, -1, 0, 1, 2, 3]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# -- Left: original grid + unit circle --
ax1.plot(np.cos(theta), np.sin(theta), 'k', linewidth=2)
for k in ks:
    lw = 2 if k == 0 else 1
    ax1.axvline(x=k, color='steelblue', linewidth=lw, alpha=0.7)
    ax1.axhline(y=k, color='indianred', linewidth=lw, alpha=0.7)
ax1.set_xlim(-4, 4)
ax1.set_ylim(-4, 4)
ax1.set_aspect('equal')
ax1.grid(False)
ax1.set_title('Grid of 14 lines + unit circle')
ax1.set_xlabel('Re(z)')
ax1.set_ylabel('Im(z)')

# -- Right: images under inversion --
ax2.plot(np.cos(theta), np.sin(theta), 'k', linewidth=2)
for k in ks:
    # Vertical x=k: c=0, alpha=1, d=-2k
    Lv = Cline(c=0, alpha=1+0j, d=-2*k)
    Lv_img = S.invert(Lv)
    # Horizontal y=k: c=0, alpha=1j, d=2k
    Lh = Cline(c=0, alpha=1j, d=2*k)
    Lh_img = S.invert(Lh)

    for img, color in [(Lv_img, 'steelblue'), (Lh_img, 'indianred')]:
        if img.is_line:
            p = img.point_on_line
            d_vec = img.direction_vector
            t = np.linspace(-2, 2, 300)
            zs = p + t * d_vec
            ax2.plot(np.real(zs), np.imag(zs), color=color, linewidth=1.5)
        elif img.is_circle:
            cx, cy = img.center.real, img.center.imag
            r = img.radius
            ax2.plot(cx + r*np.cos(theta), cy + r*np.sin(theta),
                     color=color, linewidth=1)

ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_aspect('equal')
ax2.grid(False)
ax2.set_title('Images under inversion in unit circle')
ax2.set_xlabel('Re(z)')
ax2.set_ylabel('Im(z)')
fig.tight_layout()
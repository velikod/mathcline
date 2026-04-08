Examples
========

Inverting a Grid in the Unit Circle
------------------------------------

The 14 lines of the grid :math:`x = k` and :math:`y = k` for :math:`k = -3, -2, \ldots, 3`
have simple cline equations:

- Vertical line :math:`x = k`: :math:`c = 0,\; \alpha = 1,\; d = -2k`
- Horizontal line :math:`y = k`: :math:`c = 0,\; \alpha = i,\; d = 2k`

Under inversion in the unit circle, lines through the origin (the axes) stay as lines,
while the other 12 lines each become a circle passing through the origin.

.. plot::
    :include-source: true
    :context: close-figs

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

Apollonius' Theorem via Cline Inversion
----------------------------------------

**Theorem.** Given three mutually tangent circles (no circle containing
the other two), there exist exactly two circles tangent to all three.

.. raw:: html

   <video width="100%" controls>
     <source src="_static/apollonius_proof.mp4" type="video/mp4">
     Your browser does not support the video tag.
   </video>

**Proof by inversion.** Pick a tangent point P of two of the three circles.
Translate so that P is at the origin. Now invert in the unit circle:

1. The two circles through the origin become **parallel lines**.
2. The third circle (not through the origin) becomes a **circle tangent to both lines**.
3. Between two parallel lines and a tangent circle, there exist exactly two
   circles tangent to all three — one above and one below.
4. Invert back and translate to recover the solution in the original picture.
   Since inversion preserves tangency, the result follows.

.. plot::
    :include-source: true
    :context: close-figs

    import matplotlib.pyplot as plt
    import numpy as np
    from cline import Cline

    theta = np.linspace(0, 2*np.pi, 300)

    # Three mutually tangent circles with different radii
    r1, r2, r3 = 1.0, 1.5, 0.8
    c1 = 0 + 0j
    c2 = (r1 + r2) + 0j
    x3 = ((r1+r3)**2 - (r2+r3)**2 + (r1+r2)**2) / (2*(r1+r2))
    y3 = np.sqrt((r1+r3)**2 - x3**2)
    c3 = x3 + 1j*y3

    # Tangent point P between C1 and C2
    P = r1 * (c2 - c1) / abs(c2 - c1)

    # Translate P to origin
    c1t, c2t, c3t = c1 - P, c2 - P, c3 - P

    # Invert in unit circle
    S = Cline.from_circle(center=0, radius=1)
    C1i = S.invert(Cline.from_circle(center=c1t, radius=r1))
    C2i = S.invert(Cline.from_circle(center=c2t, radius=r2))
    C3i = S.invert(Cline.from_circle(center=c3t, radius=r3))

    # Line positions
    x_l1 = -C1i.d / (2*np.real(C1i.alpha))
    x_l2 = -C2i.d / (2*np.real(C2i.alpha))

    # Solution circles in inverted picture
    mid_x = (x_l1 + x_l2) / 2
    r_sol = abs(x_l2 - x_l1) / 2
    cx3i, cy3i, r3i = C3i.center.real, C3i.center.imag, C3i.radius
    dx = mid_x - cx3i
    dy = np.sqrt(max(0, (r_sol + r3i)**2 - dx**2))

    A1i = Cline.from_circle(center=complex(mid_x, cy3i + dy), radius=r_sol)
    A2i = Cline.from_circle(center=complex(mid_x, cy3i - dy), radius=r_sol)

    # Invert back and translate
    A1t = S.invert(A1i)
    A2t = S.invert(A2i)
    A1_c, A1_r = A1t.center + P, A1t.radius
    A2_c, A2_r = A2t.center + P, A2t.radius

    # --- 4-panel proof ---
    fig, axes = plt.subplots(1, 4, figsize=(24, 6.5))

    def dc(ax, c, r, co='steelblue', lw=1.5, lb=None):
        ax.plot(np.real(c)+r*np.cos(theta), np.imag(c)+r*np.sin(theta),
                color=co, linewidth=lw, label=lb)

    # Step 1: original
    ax = axes[0]
    dc(ax, c1, r1, 'steelblue', lb='$A\\ (r=1)$')
    dc(ax, c2, r2, 'teal', lb='$B\\ (r=1.5)$')
    dc(ax, c3, r3, 'mediumpurple', lb='$C\\ (r=0.8)$')
    ax.plot(P.real, P.imag, 'ko', ms=6)
    ax.text(P.real+0.08, P.imag-0.18, '$P$', fontsize=11)
    ax.set_aspect('equal'); ax.grid(True, alpha=0.2)
    ax.set_xlim(-1.5, 4.5); ax.set_ylim(-1.5, 3)
    ax.set_title('Step 1: Three tangent circles', fontweight='bold')
    ax.legend(fontsize=8)

    # Step 2: translated + inverted
    ax = axes[1]
    ax.axvline(x=x_l1, color='steelblue', lw=1.5, label="$A'$")
    ax.axvline(x=x_l2, color='teal', lw=1.5, label="$B'$")
    dc(ax, C3i.center, C3i.radius, 'mediumpurple', lb="$C'$")
    ax.set_aspect('equal'); ax.grid(True, alpha=0.2)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.2, 2.2)
    ax.set_title('Step 2: Translate + invert', fontweight='bold')
    ax.legend(fontsize=9, loc='lower right')

    # Step 3: add solution circles
    ax = axes[2]
    ax.axvline(x=x_l1, color='steelblue', lw=1.5)
    ax.axvline(x=x_l2, color='teal', lw=1.5)
    dc(ax, C3i.center, C3i.radius, 'mediumpurple')
    dc(ax, A1i.center, A1i.radius, 'crimson', 2.5, 'Solution 1')
    dc(ax, A2i.center, A2i.radius, 'orangered', 2.5, 'Solution 2')
    ax.set_aspect('equal'); ax.grid(True, alpha=0.2)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.2, 2.2)
    ax.set_title('Step 3: Find tangent circles', fontweight='bold')
    ax.legend(fontsize=9, loc='lower right')

    # Step 4: invert back + translate
    ax = axes[3]
    dc(ax, c1, r1, 'steelblue', lw=1)
    dc(ax, c2, r2, 'teal', lw=1)
    dc(ax, c3, r3, 'mediumpurple', lw=1)
    dc(ax, A1_c, A1_r, 'crimson', 2.5, 'Solution 1')
    dc(ax, A2_c, A2_r, 'orangered', 2.5, 'Solution 2')
    ax.set_aspect('equal'); ax.grid(True, alpha=0.2)
    ax.set_xlim(-2, 5); ax.set_ylim(-3, 3)
    ax.set_title('Step 4: Invert back + translate', fontweight='bold')
    ax.legend(fontsize=9)

    fig.suptitle("Apollonius' Theorem: visual proof via cline inversion",
                 fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()

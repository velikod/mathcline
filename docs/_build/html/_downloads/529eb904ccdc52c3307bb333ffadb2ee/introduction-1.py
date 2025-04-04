import matplotlib.pyplot as plt
import numpy as np

from cline import Cline

# Create a figure
fig, ax = plt.subplots(figsize=(8, 6))

# Create several clines
circle1 = Cline.from_circle(center=0, radius=2)
circle2 = Cline.from_circle(center=2 + 1j, radius=1.5)

# For lines, we need to ensure we're using correct parameters
line1 = Cline.from_line(z0=-3 + 0j, z1=3 + 0j)  # Horizontal line
line2 = Cline.from_line(z0=0 - 3j, z1=0 + 3j)  # Vertical line

# Plot all clines
circle1.plot(ax=ax, color="royalblue", label="Circle 1")
circle2.plot(ax=ax, color="cornflowerblue", label="Circle 2")
line1.plot(ax=ax, color="firebrick", label="Line 1")
line2.plot(ax=ax, color="indianred", label="Line 2")

# Customize the plot
ax.set_xlim(-3, 4)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.7)
plt.title("Examples of Clines in the Complex Plane")
plt.legend(loc="upper right")

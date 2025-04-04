import matplotlib.pyplot as plt
import numpy as np

from cline import Cline

# Create a figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

# Example 1: A simple circle
circle = Cline.from_circle(center=0, radius=2)
circle.plot(ax=axes[0], color="blue")
axes[0].set_title("Simple Circle")
axes[0].set_aspect("equal")
axes[0].grid(True, linestyle="--", alpha=0.7)

# Example 2: A simple line
line = Cline.from_line(z0=-2, z1=2)
line.plot(ax=axes[1], color="red")
axes[1].set_title("Simple Line")
axes[1].set_aspect("equal")
axes[1].grid(True, linestyle="--", alpha=0.7)

# Example 3: Circle through three points
points = Cline.from_three_points(0, 2, 1 + 1j)
points.plot(ax=axes[2], color="green", show_points=True)
axes[2].set_title("Circle Through Points")
axes[2].set_aspect("equal")
axes[2].grid(True, linestyle="--", alpha=0.7)

# Example 4: Multiple circles
centers = [1 + 1j, -1 - 1j, -1 + 1j, 1 - 1j]
for i, c in enumerate(centers):
    Cline.from_circle(center=c, radius=0.8).plot(
        ax=axes[3], color=plt.cm.tab10(i), label=f"Circle {i+1}"
    )
axes[3].set_title("Multiple Circles")
axes[3].set_aspect("equal")
axes[3].grid(True, linestyle="--", alpha=0.7)
axes[3].legend()

# Adjust layout
plt.tight_layout()
plt.suptitle("Various Cline Examples", y=1.02, fontsize=16)
plt.subplots_adjust(top=0.9)
